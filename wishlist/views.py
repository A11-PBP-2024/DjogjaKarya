from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist
from product.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {"wishlist": wishlist_items}
    return render(request, "wishlist.html", context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist:show_wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist:show_wishlist')