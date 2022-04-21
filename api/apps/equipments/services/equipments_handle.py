from apps.equipments.models import Material

def update_materials(material_ids: list[int], materials):
    update_materials_list = []
    materials_mapping = {material["material_id"]: material for material in materials}
    materials_exists = Material.objects.filter(id__in=material_ids)
    
    for material in materials_exists:
        m = materials_mapping.get(material.id)
        amount = material.amount + m["amount"]
        update_materials_list.append(Material(id=material.id, amount=amount))
    Material.objects.bulk_update(update_materials_list, ["amount"])
