import uuid
from django.db import models


# Create your models here.
class RawBlogsEntries(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    main_image_url = models.TextField()
    title = models.TextField()
    subtitle = models.TextField()
    info_subtitles = models.JSONField()
    info_data = models.TextField()
    
class BlogProcessedEntries(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.JSONField()
