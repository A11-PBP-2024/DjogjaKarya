# DJOGJAKARYA/review/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from product.models import Product
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

@login_required
def review_list(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    similar_product = Product.objects.filter(kategori=product.kategori).exclude(id=product.id)
    return render(request, 'detail.html', {'product': product, 'reviews': reviews, 'similar_product' : similar_product })

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('review_list', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})
