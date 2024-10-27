
from django.shortcuts import get_object_or_404, render, redirect
from product.models import Product, Category
from merchant.models import Store
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
import random
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from .models import Product
from wishlist.models import Wishlist  # Mengimpor Wishlist dari aplikasi wishlist
import random



from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_superuser  # Cek apakah user adalah superuser

@csrf_exempt
@user_passes_test(is_admin)  # Hanya admin yang bisa akses
@user_passes_test(is_admin)
def get_form_data(request):

    try:
        categories = [
            'Batik', 'Kerajinan Kulit', 'Perak Kotagede', 'Kerajinan Wayang',
            'Kerajinan Kayu', 'Kerajinan Anyaman', 'Kerajinan Gerabah',
            'Kerajinan Bambu', 'Kain Tenun Lurik'
        ]
        stores = list(Store.objects.values_list('name', flat=True))
        
        return JsonResponse({
            'categories': categories,
            'stores': stores
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Validasi input
        required_fields = ['name', 'kategori', 'harga', 'toko', 'image']
        for field in required_fields:
            if not request.POST.get(field):
                return JsonResponse(
                    {'error': f'Field {field} is required'}, 
                    status=400
                )
        
        # Create new product
        product = Product.objects.create(
            name=request.POST.get('name'),
            kategori=request.POST.get('kategori'),
            harga=request.POST.get('harga'),
            toko=request.POST.get('toko'),
            image=request.POST.get('image')
        )
        
        return JsonResponse({
            'message': 'Produk berhasil ditambahkan!',
            'product': {
                'id': product.id,
                'name': product.name,
                'kategori': product.kategori,
                'harga': product.harga,
                'toko': product.toko,
                'image': product.image
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@user_passes_test(is_admin)  
@login_required
def edit_product(request, id):
    try:
       
        product = get_object_or_404(Product, id=id)

        if request.method == 'POST':
            name = request.POST.get('name')
            kategori = request.POST.get('kategori')
            harga = request.POST.get('harga')
            toko = request.POST.get('toko')
            image = request.FILES.get('image')  
            
            product.name = name
            product.kategori = kategori
            product.harga = harga
            product.toko = toko

            if image:
                product.image = image

            product.save()

            return JsonResponse({'message': 'Produk berhasil diperbarui!', 'product_id': product.id}, status=200)

        data = {
            'product': {
                'id': product.id,
                'name': product.name,
                'kategori': product.kategori,
                'harga': product.harga,
                'toko': product.toko,
                'image': product.image,
            },
            'categories': [
                'Batik', 'Kerajinan Kulit', 'Perak Kotagede', 'Kerajinan Wayang',
                'Kerajinan Kayu', 'Kerajinan Anyaman', 'Kerajinan Gerabah',
                'Kerajinan Bambu', 'Kain Tenun Lurik'
            ],
            'stores': list(Store.objects.values_list('name', flat=True))
        }
        return JsonResponse(data)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produk tidak ditemukan.'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
@user_passes_test(is_admin) 
@login_required
@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_product(request, id):
    try:
       
        product = get_object_or_404(Product, id=id)
        
        if request.user.is_superuser:
            product.delete()
            return JsonResponse({'message': 'Produk berhasil dihapus!'})
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
            
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_product(request):

    products = Product.objects.all()

    return HttpResponse(serializers.serialize("json", products), content_type="application/json")


def get_product_id(request, id):
    try:
        product = Product.objects.get(id=id)
        product_data = {
            'id': product.id,
            'name': product.name,
            'kategori': product.kategori,
            'harga': product.harga,
            'toko': product.toko,
            'image': product.image,
        }
        return JsonResponse(product_data)
    except Product.DoesNotExist:
        return HttpResponseBadRequest('Produk tidak ditemukan!')

 
def show_detail(request, id):
    selected_product = Product.objects.get(pk=id)
    kategori = selected_product.kategori
    all_products = Product.objects.filter(kategori__icontains=kategori).exclude(pk=id)

    if all_products.count() >= 3:
        similar_products = random.sample(list(all_products), 3)
    else:
        similar_products = all_products

    # Check if product is in wishlist
    in_wishlist = Wishlist.objects.filter(user=request.user, product=selected_product).exists() if request.user.is_authenticated else False

    context = {
        'product': selected_product,
        'similar_product': similar_products,
        'in_wishlist': in_wishlist,
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

