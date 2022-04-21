from django.db import transaction
from rest_framework import serializers
from apps.equipments.models import Equipment, Material, Supplier, Bill, BillDetail
from apps.equipments.exceptions import MaterialNotEmptyException, MaterialDoesNotExistsException
from apps.equipments.services.equipments_handle import update_materials


class EquipmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    buying_price = serializers.DecimalField(max_digits=11, decimal_places=0)
    
    class Meta:
        model = Equipment
        fields = ("id", "name", "buying_price", "quantity", "status", "total_buying_price")
        
        
class MaterialSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    buying_price = serializers.DecimalField(max_digits=11, decimal_places=0)
    unit = serializers.CharField(max_length=50, required=True)
    amount = serializers.FloatField(required=True)
    
    class Meta:
        model = Material
        fields = ("id", "name", "amount", "unit", "buying_price", "status")
        

class SupplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Supplier
        fields = ("id", "address", "phone",)
        
  
class BillDetailSerializer(serializers.Serializer):
    material_id = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Material.objects.all().values_list("id", flat=True), write_only=True)
    amount = serializers.FloatField(required=True)
    buying_price = serializers.DecimalField(required=True, decimal_places=0, max_digits=11)
    
    @classmethod
    def validate_material_id(cls, id):
        try:
            return Material.objects.get(id=id).id
        except Material.DoesNotExist:
            raise MaterialDoesNotExistsException()
  

class ListBillDetailSerializers(serializers.ModelSerializer):
    materials = MaterialSerializer()
    
    class Meta:
        model = BillDetail
        fields = ("id", "materials", "amount", "buying_price", "total_money")
            
        
class BillSerializer(serializers.ModelSerializer):
    materials = BillDetailSerializer(required=True, many=True, write_only=True)
    date_input   = serializers.DateTimeField(required=True)
    is_payment   = serializers.BooleanField(required=True)
    supplier_id  = serializers.PrimaryKeyRelatedField(
        required=True, source="supplier", queryset=Supplier.objects.all().values_list("id", flat=True), write_only=True)
    supplier     = SupplierSerializer(read_only=True)
    bill_details   = ListBillDetailSerializers(many=True, read_only=True)
    
    class Meta:
        model = Bill
        fields = ("id", "date_input", "is_payment", "supplier", "materials", "supplier_id", "bill_details")
    
    @transaction.atomic
    def create(self, validated_data):
        materials = list(validated_data.pop("materials"))
        validated_data.pop("supplier")
        bill = Bill.objects.create(**validated_data)
        bill_detail = []
        material_ids = []
        for m in materials:
            material_ids.append(m["material_id"])
            bill_detail.append(BillDetail(bill=bill, materials_id=m["material_id"], amount=m["amount"], buying_price=m["buying_price"]))
        BillDetail.objects.bulk_create(bill_detail)
        update_materials(material_ids, materials)
        return bill
    
 #1. Create Bill ok
 #2. List Materials (amount, buying_price) use bulk_create ok 
 #3. Update amount in materials 
    
        