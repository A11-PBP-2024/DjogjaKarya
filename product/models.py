from django.db import models

# Create your models here.
class Product (models.Model):

    name = models.CharField(max_length=200)
    kategori = models.CharField(max_length=200)
    harga = models.IntegerField()
    toko = models.CharField(max_length=200)
    image = models.TextField()


class Category (models.Model):
    name = models.CharField(max_length=200)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, name='products')
    is_wishlist = models.BooleanField(default=False)