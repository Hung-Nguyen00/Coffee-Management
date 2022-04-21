from django.urls import path
from apps.staff.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("staff", views.StaffView)
router.register("position", views.PositionView)

get_or_create_schedule = views.ScheduleStaffView.as_view({"get": "list", "post": "create"})

urlpatterns = [
    path("schedule/", get_or_create_schedule, name="get-create-schedule"),
    path("schedule/<pk>/", views.ScheduleStaffUpdateView.as_view(), name="edit-schedule"),
    path("income-history-staff/<pk>/", views.IncomeHistoryRetrieveUpdateView.as_view(), name="get-update-history-income"),
    path("income-history-staff/", views.IncomeHistoryListView.as_view(), name="list-history-income")
] + router.urls
