from threading import main_thread
from apps.equipments.models import Material, Bill, BillDetail
from typing import Dict, List



class MaterialService:
    
    @staticmethod
    def update_material_when_create_bill(material_ids: list[int], materials: Dict):
        update_materials_list = []
        materials_mapping = {material["material_id"]: material for material in materials}
        materials_exists = Material.objects.filter(id__in=material_ids)
    
        for material in materials_exists:
            m = materials_mapping.get(material.id)
            amount = material.amount + m["amount"]
            update_materials_list.append(Material(id=material.id, amount=amount))
        Material.objects.bulk_update(update_materials_list, ["amount"])
    
    @staticmethod
    def update_material_when_update_or_delete_bill_detail(update_bill_details: Dict, old_bill_detail: Dict, materials_exists: Dict):
        list_updates = []
        # if there are updating meterials, we take ids to get ORM
        material_updated_ids = [detail.material_id for detail in update_bill_details]
        # if there are removing materials, we take ids to get ORM
        materials_id     = materials_exists.values_list("material_id", flat=True)
        material_removed = [key for key, value in old_bill_detail.items() if key not in materials_id]
        
        #get concat 2 above list to get ORM
        material_ids = material_updated_ids + material_removed
        materials    = Material.objects.filter(pk__in=material_ids)
        #use map for get object 
        materials_mapping = {material.id: material for material in materials}
        
        #update materials's amount when update only amount
        for d in update_bill_details:
            material_exist       = materials_mapping.get(d.id)
            old_bill_detail_item = old_bill_detail.get(d.id)
            amount               = (material_exist - old_bill_detail_item["amount"]) + d.amount
            list_updates.append(Material(id=d.id, amount=amount))
        
        #minus amount when meterials in a bill was removed
        for matrial_id in material_removed:
            material_exist       = materials_mapping.get(matrial_id)
            old_bill_detail_item = old_bill_detail.get(matrial_id)
            amount               = material_exist.amount - old_bill_detail_item["amount"]
            list_updates.append(Material(id=matrial_id, amount=amount))
                
        Material.objects.bulk_update(list_updates, ["amount"])
                
    @staticmethod
    def update_material_when_create_bill_detail(new_bill_detail):
        #plus amount when meterials in a bill was created
        material_ids = [detail.material_id for detail in new_bill_detail]
        materials = Material.objects.filter(pk__in=material_ids)
        materials_mapping = {material.id: material for material in materials}
        list_updates = []
        for n in new_bill_detail:
            material = materials_mapping.get(n.material_id)
            amount = material.amount + n.amount
            list_updates.append(Material(id=n.material_id, amount=amount))
        
        Material.objects.bulk_update(list_updates, ["amount"])
        
    
    @staticmethod
    def update_material_when_remove_or_update_bill_detail(bill_details_data: Dict, instance: Bill):
        #remove material do not exist and take material existing to update
        materials_id = [material.get("material_id") for material in bill_details_data if material.get("material_id") is not None]
        
        # get all bill_detail from instance
        bill_detail =  BillDetail.objects.filter(bill=instance).all()
        old_bill_detail = {detail.material_id: {"amount": detail.amount} for detail in bill_detail}
        bill_detail.exclude(id__in=materials_id).delete()
        materials_exists = bill_detail.filter(id__in=materials_id)
        mapping_material = {detail.id: detail for detail in materials_exists}
        
        update_bill_details = []
        new_bill_details = []
        for m in bill_details_data:
            buying_price = m["buying_price"]
            amount = m["amount"]
            material_id = m["material_id"]
            get_material = mapping_material.get(material_id)
            #if item exists -> update
            if get_material:
                if get_material.amount != amount or get_material.buying_price != buying_price:
                    bill_detail = BillDetail(id=get_material.id, material_id=m["material_id"], amount=amount, buying_price=buying_price)
                    update_bill_details.append(bill_detail)
            #if item doesn't exist -> create 
            else: 
                bill_detail = BillDetail(bill=instance, material_id=m["material_id"], amount=amount, buying_price=buying_price)
                new_bill_details.append(bill_detail)
        #create and update multiple items
        if len(update_bill_details) > 0:
            BillDetail.objects.bulk_update(update_bill_details, ["amount", "buying_price"])
            
        if len(new_bill_details) > 0:
            BillDetail.objects.bulk_create(new_bill_details)
            MaterialService.update_material_when_create_bill_detail(new_bill_details)
            
        MaterialService.update_material_when_update_or_delete_bill_detail(update_bill_details, old_bill_detail, materials_exists)    
        
        return instance
        