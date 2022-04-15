import django_filters.rest_framework as django_filters
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.utils import get_logger
from apps.notification.api import serializers
from apps.notification.services import query, usercases

logger = get_logger(__name__)


class MessageListView(generics.ListAPIView):
    serializer_class = serializers.MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.DjangoFilterBackend]
    filterset_fields = ["status", "read"]
    search_fields = ["category__name", "topic", "title", "content", "status"]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return query.get_visible_messages_queryset(user=self.request.user)


class MessageReadView(APIView):
    """
    parameters
    - ids: [id1, id2, id3, ...]: A list of notification ID
    - all: (Y/N) : if marked as read all notifications
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        notification_ids = request.data.get("ids", [])
        read_all = request.data.get("all", usercases.YesNo.NO)

        usercases.MarkNotificationAsRead(user=request.user, ids=notification_ids, read_all=read_all).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageArchiveView(APIView):
    """
    parameters
    - ids: [id1, id2, id3, ...]: A list of notification ID
    - all: (Y/N) : if archive all notifications
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        notification_ids = request.data.get("ids", [])
        archive_all = request.data.get("all", usercases.YesNo.NO)
        usercases.ArchiveNotification(user=request.user, ids=notification_ids, archive_all=archive_all).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageBadgeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        totals = query.get_unread_messages_queryset(user=self.request.user).count()
        return Response({"badge": totals}, status=status.HTTP_200_OK)
