import django_filters.rest_framework as django_filters
from django.db import transaction
from drf_yasg.openapi import IN_QUERY, Items, Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import InvalidParameterException, ObjectNotFoundException
# from apps.hr.models import Employee
# from apps.hr.permissions import AllowHR, AllowPM, AllowStaff
from apps.users import services
from apps.users.api import serializers
from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="is_active", method="status_custom_filter")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["email", "status"]

    def status_custom_filter(self, queryset, value, *args, **kwargs):
        try:
            if args:
                status_param = args[0].split(",")
                if status_param[0] == "active":
                    queryset = queryset.filter(is_active=True)
                elif status_param[0] == "inactive":
                    queryset = queryset.filter(is_active=False)
                elif status_param[0] == "all":
                    queryset
        except ValueError:
            pass
        return queryset


# class UserView(
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet,
# ):
#     serializer_class = serializers.UserSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.DjangoFilterBackend]
#     filterset_class = UserFilter
#     ordering_fields = "__all__"
#     search_fields = ["email"]
#     queryset = User.objects.all()
#     lookup_field = "id"
#     http_method_names = ["get", "patch", "post", "delete"]
#     # permission_classes = (AllowHR,)

#     @swagger_auto_schema(operation_summary="Create new User")
#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         password = request.data.pop("password")
#         user = serializer.save()
#         user.set_password(password)
#         user.save()
#         return Response(serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(operation_summary="Get User list")
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)

#     @swagger_auto_schema(operation_summary="Get User by uuid")
#     def retrieve(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)

#     @swagger_auto_schema(operation_summary="Update User by uuid")
#     @transaction.atomic
#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)

#     @swagger_auto_schema(operation_summary="Delete User by uuid")
#     def destroy(self, request, *args, **kwargs):
#         # Avoid current user from self-deleting
#         current_user = self.request.user
#         instance = self.get_object()
#         superusers = User.objects.filter(is_superuser=True)
#         if current_user == instance:
#             raise InvalidParameterException("You can not delete yourself!")
#         if len(superusers) == 1 and instance == superusers[0]:
#             raise InvalidParameterException("There is at least one superuser exist!")
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class UserProfileView(generics.RetrieveAPIView):
#     serializer_class = serializers.UserSerializer
#     permission_classes = (AllowHR | AllowPM | AllowStaff,)

#     def get_object(self):
#         return self.request.user


# class UpdateUserProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = serializers.UserSerializer
#     permission_classes = (AllowHR | AllowPM | AllowStaff,)

#     def get_object(self):
#         return self.request.user


class UserExistView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="check exist email or username",
        operation_id="username_email_exist",
        security=[],
    )
    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        email = request.query_params.get("email")

        exists = services.exists_user(username=username, email=email)
        data = {"exists": exists}
        return Response(data, status=status.HTTP_200_OK)


class UserRolesView(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get("uid"))
        data = services.get_user_roles(user)
        return Response(data, status=status.HTTP_200_OK)


class UpdateUserRolesView(generics.CreateAPIView, generics.DestroyAPIView):
    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get("uid"))
        role_name = self.kwargs.get("name")
        data = services.assign_user_role(user, role_name)
        return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get("uid"))
        role_name = self.kwargs.get("name")
        services.remove_user_role(user, role_name)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionsView(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get("uid"))
        data = services.get_user_permissions(user)
        return Response(data, status=status.HTTP_200_OK)


# class DeleteUserView(generics.GenericAPIView):
#     serializer_class = serializers.UserSerializer
#     permission_classes = (AllowHR,)

#     @swagger_auto_schema(
#         operation_summary="Delete Multiple Users",
#         responses={204: ""},
#         manual_parameters=[
#             Parameter("id", IN_QUERY, type="array", items=Items("string")),
#         ],
#     )
#     def delete(self, request, *args, **kwargs):
#         ids = self.request.query_params.get("id").split(",")
#         if not ids:
#             raise ObjectNotFoundException("Object not found")
#         for id in ids:
#             user = User.objects.filter(pk=id).first()
#             Employee.objects.filter(user=id).delete()
#             user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
