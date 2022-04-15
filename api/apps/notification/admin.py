from django.contrib import admin

from apps.notification.models import Category, Message


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created",
        "modified",
    )
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "user",
        "verb",
        "title",
        "content",
        "status",
        "sent_date",
    )
    search_fields = (
        "user__username",
        "verb",
    )
    raw_id_fields = (
        "user",
        "actor",
        "category",
    )
    ordering = ("-created",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "category")
