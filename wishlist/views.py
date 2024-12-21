from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse


@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    # Serialize data
    data = serializers.serialize('json', wishlist_items, use_natural_foreign_keys=True)
    # Return JSON response
    return JsonResponse({'wishlist': data}, safe=False)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        return JsonResponse({'message': 'Item added to wishlist'}, status=201)
    else:
        return JsonResponse({'message': 'Item already in wishlist'}, status=200)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    deleted, _ = Wishlist.objects.filter(user=request.user, product=product).delete()
    if deleted:
        return JsonResponse({'message': 'Item removed from wishlist'}, status=200)
    else:
        return JsonResponse({'message': 'Item not found in wishlist'}, status=404)
