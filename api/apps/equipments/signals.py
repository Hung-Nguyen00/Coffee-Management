from django.dispatch import Signal, receiver
from apps.equipments.models import BillDetail, Material
from django.db.models.signals import pre_save, post_save, post_delete

dispatch_uploaded_material = Signal(providing_args=["bill_details", "old_bill_detail"])

# @receiver(dispatch_uploaded_material)
# def update_amount_of_material_when_update_a_bill_detail(sender, **kwargs):
#     bill_details = kwargs["bill_details"]
#     old_bill_detail = kwargs["old_bill_detail"]
    
#     material_ids = [detail.id for detail in bill_details]
#     material_removed = [old_detail for old_detail in old_bill_detail if old_detail.keys() not in material_ids]
#     materials = Material.objects.filter(pk__in=material_ids)
#     materials_exist_mapping = {material.id: material for material in materials}
#     list_updates = []
#     for d in bill_details:
#         material_exist = materials_exist_mapping.get(d.id)
#         old_bill_detail = old_bill_detail.get(d.id)
#         amount = (material_exist - old_bill_detail.amount) + d.amount
#         list_updates.append(Material(id=d.id, amount=amount))
        
#     for r in material_removed:
#         material_exist = materials_exist_mapping.get(d.id)
#         old_bill_detail = old_bill_detail.get(d.id)
#         amount = material_exist.amount - old_bill_detail.amount
#         list_updates.append(Material(id=d.id, amount=amount))
        
#     Material.objects.bulk_update(list_updates, ["amount"])
        
@receiver(pre_save, sender=BillDetail)
def update_amount_material_when_upload_bill_detail(sender, **kwargs):
    print("12******")
    
@receiver(post_save, sender=BillDetail)
@receiver(post_delete, sender=BillDetail)
def update_amount_material_when_post_save_bill_detail(sender, **kwargs):
    print("13******")
