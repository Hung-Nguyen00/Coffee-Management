from django.dispatch import Signal

dispatch_uploaded_file = Signal(providing_args=["uploaded_file"])

dispatch_mark_file_used = Signal(providing_args=["uploaded_file"])

dispatch_mark_file_deleted = Signal(providing_args=["uploaded_file"])

dispatch_create_thumbnail = Signal(providing_args=["uploaded_file"])
