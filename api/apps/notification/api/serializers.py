from rest_framework import serializers

from apps.notification.models import Category, Message


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class MessageSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)

    class Meta:
        model = Message
        fields = (
            "id",
            "category",
            "verb",
            "title",
            "content",
            "status",
            "read",
            "created",
        )
