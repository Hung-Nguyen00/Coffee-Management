from apps.orders.models import Order

def create_order_code() -> str:
    last_order = Order.objects.all().last()
    order_id = str(last_order.id + 1) if last_order else "1"
    len_id = int(len(order_id))
    return "0".join("" for _ in range(0, 10-len_id)) + order_id

    