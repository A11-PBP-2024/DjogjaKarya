from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Store
from .forms import StoreForm
from django.core import serializers
from product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

def is_admin(user):
    return user.is_superuser 

@login_required
def get_user_status(request):
    return JsonResponse({
        'is_admin': is_admin(request.user)
    })

@login_required
def store_list(request):
    return render(request, 'store_list.html')

@login_required
def get_stores(request):
    data = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
    content_type="application/json")

def store_detail(request, id):
    store = get_object_or_404(Store, id=id)
    context = {
        'store': store
    }
    return render(request, 'store_detail.html', context)


@csrf_exempt
@login_required
@user_passes_test(is_admin)
def add_store(request):
    name = request.POST.get("name")
    description = request.POST.get("description")
    address = request.POST.get("address")
    opening_days = request.POST.get("opening_days")
    opening_hours = request.POST.get("opening_hours")
    phone = request.POST.get("phone")
    image1 = request.POST.get("image1")
    image2 = request.POST.get("image2")
    image3 = request.POST.get("image3")
    location_link = request.POST.get("location_link")

    new_store = Store(name=name, description=description, address=address,
                      opening_days=opening_days, opening_hours=opening_hours, phone=phone,
                      image1=image1, image2=image2, image3=image3,location_link=location_link)

    new_store.save()
    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def edit_store(request, id):
    store = get_object_or_404(Store, id=id)

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('merchant:store_list')
    else:
        form = StoreForm(instance=store)

    context = {
        'form': form,
        'store': store
    }
    return render(request, 'edit_store.html', context)

@csrf_exempt
@login_required
@user_passes_test(is_admin)  
def delete_store(request, id):
    store = Store.objects.get(pk = id)
    store.delete()
    return HttpResponseRedirect(reverse('merchant:store_list'))

def store_products(request):
    store_name = request.GET.get('toko')
    products = Product.objects.filter(toko=store_name)
    context = {
        'products': products,
        'selected_store': store_name
    }
    return render(request, 'store_products.html', context)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def create_store_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_store = Store.objects.create(
            name=data["name"],
            description=data["description"],
            address=data["address"],
            opening_days=data["opening_days"],
            opening_hours=data["opening_hours"],
            phone=data["phone"],
            image1=data["image1"],
            image2=data["image2"],
            image3=data["image3"],
            location_link=data["location_link"],
        )
        new_store.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def edit_store_flutter(request, id):
    if request.method == 'POST':
        try:
            store = Store.objects.get(pk=id)
            data = json.loads(request.body)

            store.name = data["name"]
            store.description = data["description"]
            store.address = data["address"]
            store.opening_days = data["opening_days"]
            store.opening_hours = data["opening_hours"]
            store.phone = data["phone"]
            store.image1 = data["image1"]
            store.image2 = data["image2"]
            store.image3 = data["image3"]
            store.location_link = data["location_link"]
            store.save()

            return JsonResponse({"status": "success"}, status=200)
        except Store.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Store not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=401)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_store_flutter(request, id):
   if request.method == 'POST':
       try:
           store = Store.objects.get(pk=id)
           store.delete()
           return JsonResponse({"status": "success"}, status=200)
       except Store.DoesNotExist:
           return JsonResponse({"status": "error", "message": "Store not found"}, status=404)
       except Exception as e:
           return JsonResponse({"status": "error", "message": str(e)}, status=400)
   return JsonResponse({"status": "error", "message": "Invalid method"}, status=401)

@csrf_exempt
@login_required
def store_products_flutter(request):
    store_name = request.GET.get('toko')
    products = Product.objects.filter(toko=store_name)
    
    products_data = json.loads(serializers.serialize('json', products))
    
    return JsonResponse({
        'products': products_data, 
        'selected_store': store_name
    })