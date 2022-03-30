from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.uploads.api.serializers import UploadFileSerializer
from apps.uploads.models import UploadFile
from apps.uploads.services.upload import upload_files
from apps.uploads.services.usercases import UploadFileService


class UploadFileView(generics.ListCreateAPIView):
    serializer_class = UploadFileSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        upload_file = upload_files(request=self.request)
        data = UploadFileSerializer(upload_file, many=True).data
        return Response(status=status.HTTP_201_CREATED, data=data)

    def get_queryset(self):
        return UploadFile.objects.all()


class S3PreSignedPost(APIView):
    @classmethod
    def get(cls, request, *args, **kwargs):
        return Response(
            UploadFileService.get_pre_signed_url(request),
            status=status.HTTP_200_OK,
        )
