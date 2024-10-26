from django.db import models
from product.models import Product

class Store(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    opening_days = models.CharField(max_length=255, null=True, blank=True)
    opening_hours = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image1 = models.URLField(null=True, blank=True)
    image2 = models.URLField(null=True, blank=True)
    image3 = models.URLField(null=True, blank=True)
    location_link = models.URLField(max_length=200, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='stores')
