from django.db import models
import uuid

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255)
    opening_days = models.CharField(max_length=255, null=True)
    opening_hours = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    image1 = models.URLField(null=True)
    image2 = models.URLField(null=True)
    image3 = models.URLField(null=True)
    location_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name
