from apps.orders.models import Menu, OrderTable, Order
from typing import Dict

def create_or_update_ordertable(order: Order, menus_data: Dict):
    menus_ids_data = [menu["menu_id"] for menu in menus_data]
    menus = Menu.objects.filter(pk__in=menus_ids_data)
    menus_mapping = {menu.id: menu for menu in menus}
    OrderTable.objects.filter(order=order).delete()
    
    list_updates = []
    for menu in menus_data:
        menu_mapping = menus_mapping.get(menu["menu_id"])
        list_updates.append(OrderTable(menu=menu_mapping, order=order, price=menu_mapping.selling_price, amount=menu["amount"]))
    OrderTable.objects.bulk_create(list_updates)   
    