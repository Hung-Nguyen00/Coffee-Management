from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.users.api import views

router = DefaultRouter()
# router.register("", views.UserView, basename="user")

urlpatterns = [
    # path("me/", views.UserProfileView.as_view(), name="me"),
    # path(
    #     "profile/",
    #     views.UpdateUserProfileView.as_view(),
    #     name="update-profile",
    # ),
    # path("exists/", views.UserExistView.as_view(), name="user-exists"),
    # path("<uid>/roles/", views.UserRolesView.as_view()),
    # path("<uid>/permissions/", views.PermissionsView.as_view()),
    # path("<uid>/roles/<name>/", views.UpdateUserRolesView.as_view()),
    # path("delete-multiple/", views.DeleteUserView.as_view()),
] + router.urls
