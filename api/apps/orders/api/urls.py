from django.urls import path
from apps.orders.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("tables", views.TableViewSet) 
router.register("menus", views.MenuViewSet) 

urlpatterns = [
    path("table/<table_id>/order/", views.OrderCreateListView.as_view(), name="order-create-list"),
    path("table/<table_id>/order/<order_id>/", views.OrderRetreivePaymentDestroyView.as_view(), name="order-retreive-payment-destroy"),
    path("table/<table_id>/order/<order_id>/menus/", views.InputOrderTableUpdateView.as_view(), name="order-update-create-menu"),
] + router.urls