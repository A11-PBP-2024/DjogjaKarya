from django.db import models
from product.models import Product

class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    opening_days = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    image1 = models.URLField()
    image2 = models.URLField()
    image3 = models.URLField()
    location_link = models.URLField(max_length=200)
    products = models.ManyToManyField(Product, related_name='stores')
