from rest_framework import serializers
from apps.orders.models import *
import datetime


class TableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Table
        fields = "__all__"
    
    
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"
        
        
class OrderTableSerializer(serializers.ModelSerializer):
    menu_id = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Menu.objects.all().values_list("id", flat=True), write_only=True
    )
    
    class Meta:
        model = OrderTable
        fields = (
            "id",
            "menu",
            "price",
            "menu_id",
            "amount",
            "total_price"
        )
        read_only_fields = (
            "menu",
            "price",
            "amount",
        )


class OrderDrinkingSerializer(serializers.Serializer):
    menu_id = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all().values_list("id", flat=True), required=True)
    amount = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    order_detail  = OrderTableSerializer(many=True, read_only=True)
    table_id      = serializers.IntegerField(write_only=True)
    table         = TableSerializer(read_only=True)
    total_price   = serializers.SerializerMethodField(read_only=True)
    paid          = serializers.BooleanField(default=False)
    paid_datetime = serializers.DateTimeField(default=None)
    
    class Meta:
        model = Order
        fields = ("id", "code", "paid", "order_detail", "table", "table_id", "paid_datetime", "total_price")
    
    @classmethod
    def get_total_price(cls, obj):
        return obj.total_price if obj.total_price else 0
        

class InputOrderTableSerializer(serializers.Serializer):
    menus = serializers.ListField(
        child=OrderDrinkingSerializer(), write_only=True, required=False
    )
    
    def validate_menus(self, value):
        menus_set = set([menu["menu_id"] for menu in value])
        if len(value) != len(menus_set):
            raise serializers.ValidationError("Every drinking is not duplicated")
        return value
    
    