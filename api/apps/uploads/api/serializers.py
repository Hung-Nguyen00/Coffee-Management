from rest_framework import serializers

from apps.uploads.models import UploadFile


class UploadFileSerializer(serializers.ModelSerializer):
    folder_name = serializers.CharField(write_only=True)
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = UploadFile
        fields = (
            "id",
            "status",
            "file_path",
            "thumbnail_path",
            "size",
            "mime_type",
            "metadata",
            "ip_address",
            "user",
            "storage",
            "url",
            "folder_name",
        )

    @classmethod
    def get_file_path(cls, obj):
        return obj.file_path.name if bool(obj.file_path) else None
