# In book/views.py
from django.shortcuts import render
from product.models import Product, Category
from django.http import JsonResponse

def show_product(request):

    product = Product.objects.all()
    context = {
    'name': request.user.username,
    'name': 'Khayla Naura Ulya Luqyana',
    'class': 'PBP A',
    'npm': '2306275310',
    'products': product,
}

    return render(request, "all.html", context)

def show_category(request):
    category = Category.objects.all().values("products")
    all_products = Product.objects.all()
    batik = Product.objects.filter(kategori__icontains="Batik")
    kulit = Product.objects.filter(kategori__icontains="Kerajinan Kulit")
    perak = Product.objects.filter(kategori__icontains="Perak Kotagede")
    wayang = Product.objects.filter(kategori__icontains="Kerajinan Wayang")
    kayu = Product.objects.filter(kategori__icontains="Kerajinan Kayu")
    anyaman = Product.objects.filter(kategori__icontains="Kerajinan Anyaman")
    gerabah = Product.objects.filter(kategori__icontains="Kerajinan Gerabah Kasongan")
    bambu = Product.objects.filter(kategori__icontains="Kerajinan Bambu")
    tenun = Product.objects.filter(kategori__icontains="Kain Tenun Lurik")

    context = {
        # 'name':,
        'categories': category,
        'books': all_products,
        'kainBatik':batik,
        'kerajinanKulit':kulit,
        'kerajinanPerak':perak,
        'kerajinanWayang': wayang,
        'kerajinanKayu': kayu,
        'kerajinanAnyaman': anyaman,
        'kerajinanGerabah': gerabah,
        'kerajinanBambu': bambu,
        'kerajinanTenun': tenun,
    }

    return render(request, "capek.html", context)
    

    
def show_detail(request, id):
    selected_product = Product.objects.get(pk=id)
    kategori = selected_product.kategori
    similar_products = Product.objects.filter(kategori__icontains=kategori).exclude(pk=id)[:6]


    # book_reviews = Review.objects.filter(book=selected_book)

    context = {
        'product': selected_product,
        # 'user': request.user.username if request.user.is_authenticated else "Guest",
        'similar_product': similar_products,
        'kategori': kategori,
        # 'selected_genres': selected_genres,
        # 'reviews': book_reviews  # Add this line
    }
    return render(request, "detail.html", context)



def show_category2(request):
    # Filter produk berdasarkan kategori
    kainBatik = list(Product.objects.filter(kategori__icontains='Batik').values())
    kerajinanKulit = list(Product.objects.filter(kategori__icontains='Kerajinan Kulit').values())
    kerajinanPerak = list(Product.objects.filter(kategori__icontains='Perak').values())
    kerajinanWayang = list(Product.objects.filter(kategori__icontains='Wayang').values())
    kerajinanKayu = list(Product.objects.filter(kategori__icontains='Kayu').values())
    kerajinanAnyaman = list(Product.objects.filter(kategori__icontains='Anyaman').values())
    kerajinanGerabah = list(Product.objects.filter(kategori__icontains='Gerabah').values())
    kerajinanBambu = list(Product.objects.filter(kategori__icontains='Bambu').values())
    kerajinanTenun = list(Product.objects.filter(kategori__icontains='Tenun').values())

    # Jika request AJAX, kembalikan JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'kainBatik': kainBatik,
            'kerajinanKulit': kerajinanKulit,
            'kerajinanPerak': kerajinanPerak,
            'kerajinanWayang': kerajinanWayang,
            'kerajinanKayu': kerajinanKayu,
            'kerajinanAnyaman': kerajinanAnyaman,
            'kerajinanGerabah': kerajinanGerabah,
            'kerajinanBambu': kerajinanBambu,
            'kerajinanTenun': kerajinanTenun,
        }
        return JsonResponse(data)

    # Jika bukan AJAX, render HTML biasa
    context = {
        'kainBatik': Product.objects.filter(kategori__icontains='Batik'),
        'kerajinanKulit': Product.objects.filter(kategori__icontains='Kerajinan Kulit'),
        'kerajinanPerak': Product.objects.filter(kategori__icontains='Perak'),
        'kerajinanWayang': Product.objects.filter(kategori__icontains='Wayang'),
        'kerajinanKayu': Product.objects.filter(kategori__icontains='Kayu'),
        'kerajinanAnyaman': Product.objects.filter(kategori__icontains='Anyaman'),
        'kerajinanGerabah': Product.objects.filter(kategori__icontains='Gerabah'),
        'kerajinanBambu': Product.objects.filter(kategori__icontains='Bambu'),
        'kerajinanTenun': Product.objects.filter(kategori__icontains='Tenun'),
    }
    return render(request, 'fix.html', context)

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

# def show_coba(request):
#     # Ambil kategori dari query string, default ke 'all' kalau tidak ada
#     kategori = request.GET.get('kategori', 'all')

#     if kategori == 'all':
#         all_products = Product.objects.all()
#     else:
#         all_products = Product.objects.filter(kategori__icontains=kategori)

#     context = {
#         'books': all_products,  # Produk yang akan ditampilkan
#         'selected_kategori': kategori,  # Untuk highlight kategori aktif
#     }

#     return render(request, "capek.html", context)

def show_coba(request):
    kategori = request.GET.get('kategori', 'all')

    # Jika kategori adalah 'all', ambil semua produk per kategori
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
        # Jika kategori spesifik dipilih, tampilkan hanya produk kategori tersebut
        products = Product.objects.filter(kategori__icontains=kategori)
        context = {
            'books': products,
            'selected_kategori': kategori,
        }

    return render(request, 'capek.html', context)
