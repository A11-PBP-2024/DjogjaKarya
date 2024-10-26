
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, Product  # Pastikan import yang benar
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)  # Sesuaikan dengan model User
    return render(request, 'wishlist.html', {'wishlist': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist:wishlist_view')

@login_required
def remove_from_wishlist(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, product_id=product_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist:wishlist_view')
