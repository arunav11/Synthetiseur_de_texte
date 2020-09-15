import uuid

from django.db import models


class MediaFile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.UUIDField(default=uuid.uuid4, editable=False, )
    photo = models.FileField(upload_to='files')
