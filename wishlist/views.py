from django.shortcuts import get_object_or_404, redirect, render
from .models import Wishlist
from product.models import Product


def show_wishlist(request):
    # Ambil wishlist untuk pengguna yang sedang login, jika ada
    wishlist_items = Wishlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('product:show_detail', product_id)

def remove_from_wishlist(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, product_id=product_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist:show_wishlist')
