
from django.shortcuts import render
from product.models import Product, Category
from django.http import JsonResponse
import random

def show_product(request):

    product = Product.objects.all()
    context = {
    'name': request.user.username,
    'name': 'Khayla Naura Ulya Luqyana',
    'class': 'PBP A',
    'npm': '2306275310',
    'products': product,
}

    return render(request, "category.html", context)

 
def show_detail(request, id):
    selected_product = Product.objects.get(pk=id)
    kategori = selected_product.kategori
    all_products = Product.objects.filter(kategori__icontains=kategori).exclude(pk=id)

    if all_products.count() >= 3:
        similar_products = random.sample(list(all_products), 3)
    else:
        similar_products = all_products

    context = {
        'product': selected_product,
        'similar_product': similar_products,
    }

    return render(request, "detail.html", context)

def filter_category_ajax(request):
    kategori = request.GET.get('kategori', 'all')

    if kategori == 'all':
        data = {
            'kainBatik': list(Product.objects.filter(kategori__icontains="Batik").values()),
            'kerajinanKulit': list(Product.objects.filter(kategori__icontains="Kerajinan Kulit").values()),
            'kerajinanPerak': list(Product.objects.filter(kategori__icontains="Perak Kotagede").values()),
            'kerajinanWayang': list(Product.objects.filter(kategori__icontains="Kerajinan Wayang").values()),
            'kerajinanKayu': list(Product.objects.filter(kategori__icontains="Kerajinan Kayu").values()),
            'kerajinanAnyaman': list(Product.objects.filter(kategori__icontains="Kerajinan Anyaman").values()),
            'kerajinanGerabah': list(Product.objects.filter(kategori__icontains="Kerajinan Gerabah Kasongan").values()),
            'kerajinanBambu': list(Product.objects.filter(kategori__icontains="Kerajinan Bambu").values()),
            'kerajinanTenun': list(Product.objects.filter(kategori__icontains="Kain Tenun Lurik").values()),
        }
    else:
        products = Product.objects.filter(kategori__icontains=kategori)
        data = {'products': list(products.values())}

    return JsonResponse(data)



def show_category(request):
    kategori = request.GET.get('kategori', 'all')

    if kategori == 'all':
        context = {
            'kainBatik': Product.objects.filter(kategori__icontains="Batik"),
            'kerajinanKulit': Product.objects.filter(kategori__icontains="Kerajinan Kulit"),
            'kerajinanPerak': Product.objects.filter(kategori__icontains="Perak Kotagede"),
            'kerajinanWayang': Product.objects.filter(kategori__icontains="Kerajinan Wayang"),
            'kerajinanKayu': Product.objects.filter(kategori__icontains="Kerajinan Kayu"),
            'kerajinanAnyaman': Product.objects.filter(kategori__icontains="Kerajinan Anyaman"),
            'kerajinanGerabah': Product.objects.filter(kategori__icontains="Kerajinan Gerabah Kasongan"),
            'kerajinanBambu': Product.objects.filter(kategori__icontains="Kerajinan Bambu"),
            'kerajinanTenun': Product.objects.filter(kategori__icontains="Kain Tenun Lurik"),
            'selected_kategori': 'all',  # Untuk highlight kategori aktif
        }
    else:

        products = Product.objects.filter(kategori__icontains=kategori)
        context = {
            'products': products,
            'selected_kategori': kategori,
        }

    return render(request, 'category.html', context)
