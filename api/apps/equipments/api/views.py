from apps.equipments.models import Equipment, Material, Supplier, Bill, BillDetail
from rest_framework import viewsets, filters, generics
from rest_framework.response import Response
from apps.equipments.api.serializers import (
    EquipmentSerializer,
    MaterialSerializer,
    BillSerializer,
    BillUpdateSerializer,
    SupplierSerializer)
import django_filters.rest_framework as django_filters
from apps.equipments.enums import EquipmentStatus, MaterialStatus
from apps.equipments.exceptions import BillDetailDoesNotExistsException
from django.db import models
from drf_yasg.utils import swagger_auto_schema



class CustomFilterEquipment(django_filters.FilterSet):
    status = django_filters.filters.MultipleChoiceFilter(choices=EquipmentStatus.choices())

    class Meta:
        model = Equipment
        fields = ["name", "status"]
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }
        

class CustomFilterMaterial(django_filters.FilterSet):
    status = django_filters.filters.MultipleChoiceFilter(choices=MaterialStatus.choices())

    class Meta:
        model = Material
        fields = ["name", "status"]
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }


class EquipmentView(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = CustomFilterEquipment
    search_fields = ["name"]

    @swagger_auto_schema(
        operation_summary="Create Equipment",
        operation_description={"status": EquipmentStatus.choices()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class MaterialView(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = CustomFilterMaterial
    search_fields = ["name"]

    @swagger_auto_schema(
        operation_summary="Create Material",
        operation_description={"status": MaterialStatus.choices()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
class SupplierView(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    search_fields = ["name"]
    

class CreateListBillView(generics.ListCreateAPIView):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    

class RetrieveUpdateDestroyBillView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BillUpdateSerializer
    queryset = Bill.objects.all()
    
    
    def patch(self, request, *args, **kwargs):
        try:
            return self.partial_update(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": f"{e}", "explanation": "Assignment not found"}, status=400)
        
    def delete(self, request, *args, **kwargs):
        try:
            if self.get_object().is_payment == False:
                return self.destroy(request, *args, **kwargs)
            else:
                return Response({"message": f"Can't not delete a bill that is paid"}, status=400)
        except Exception as e:
            return Response({"message": f"{e}", "explanation": "Assignment not found"}, status=400)