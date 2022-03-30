from django.urls import path

from apps.uploads.api.views import S3PreSignedPost, UploadFileView

urlpatterns = [
    path("", UploadFileView.as_view(), name="upload-file"),
    path("s3/pre-signed-post-url", S3PreSignedPost.as_view()),
]
