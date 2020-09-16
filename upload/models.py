import uuid

from django.db import models


class MediaFile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, )
    file = models.FileField(upload_to='files')
    summary = models.TextField(default="")
    questions = models.TextField(default="")
