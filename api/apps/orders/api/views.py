from rest_framework import viewsets, filters, generics, serializers
from apps.orders.api.serializers import TableSerializer, MenuSerializer, OrderSerializer, InputOrderTableSerializer
import django_filters.rest_framework as django_filters
from apps.orders.models import Table, Menu, Order
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.orders.libs import create_order_code
from apps.orders.services.function_handlers import create_or_update_ordertable
from drf_yasg.utils import swagger_auto_schema


class TableViewSet(viewsets.ModelViewSet):
    serializer_class = TableSerializer
    filter_backends  = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    queryset = Table.objects.all()
    
    
class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    filter_backends  = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    queryset = Menu.objects.all()
    

class OrderCreateListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    
    def get_queryset(self):
        table_id = self.kwargs.get("table_id")
        return Order.objects.filter(table_id=table_id)
    
    @swagger_auto_schema(
        operation_summary="Create order when a table order drinking"
    )
    def post(self, request, *args, **kwargs):
        table_id = kwargs.get("table_id")
        try:
            table = Table.objects.get(pk=table_id)
        except Table.DoesNotExist as e:
            raise serializers.ValidationError({"message": f"Error {e}"})
        if table.is_active:
            raise serializers.ValidationError("There is a customer who is sitting this table")
        request.data["table_id"] = table_id
        request.data["code"] = create_order_code()
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**request.data)
        
        table.is_active = False
        table.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderRetreivePaymentDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class  = OrderSerializer
    queryset          = Order.objects.all()
    lookup_field      = "order_id"
    http_method_names = ["get", "patch", "delete"]
    
    def get_object(self):
        table_id = self.kwargs["table_id"]
        order_id = self.kwargs["order_id"]
        filter = {"pk": order_id, "table_id": table_id, "paid": False}
        return get_object_or_404(Order, **filter)
    
    
class InputOrderTableUpdateView(generics.UpdateAPIView):
    serializer_class  = InputOrderTableSerializer
    queryset          = Order.objects.all()
    lookup_field      = "order_id"
    http_method_names = ["patch"]
    
    def get_object(self):
        table_id = self.kwargs["table_id"]
        order_id = self.kwargs["order_id"]
        filter = {"pk": order_id, "table_id": table_id, "paid": False}
        return get_object_or_404(Order, **filter)

    @swagger_auto_schema(
        operation_summary="Order drinking from menu. menu_ids must exist in ids of menu table"
    )
    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        menus_data = request.data.pop("menus")
        create_or_update_ordertable(order, menus_data)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
