from django.urls import path
from apps.equipments.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("equipments", views.EquipmentView)
router.register("materials", views.MaterialView)
router.register("suppliers", views.SupplierView)

urlpatterns = [
    path("materials/bill/", views.CreateListBillView.as_view(), name="list-create-bill"),
    path("materials/bill/<pk>/", views.RetrieveUpdateDestroyBillView.as_view(), name="update-retreive-destroy")
] + router.urls
