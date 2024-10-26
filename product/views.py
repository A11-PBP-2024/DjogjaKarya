# In book/views.py
from django.shortcuts import render
from product.models import Product

def show_product(request):

    product = Product.objects.all()
    context = {
    'name': request.user.username,
    'name': 'Khayla Naura Ulya Luqyana',
    'class': 'PBP A',
    'npm': '2306275310',
    'products': product,
}

    return render(request, "niru.html", context)
