from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Store
from .forms import StoreForm
from django.core import serializers
from product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def store_list(request):
    return render(request, 'store_list.html')

def get_stores(request):
    data = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
    content_type="application/json")

@csrf_exempt
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

def edit_store(request, id):
    store = Store.objects.get(pk = id)
    form = StoreForm(request.POST or None, instance=store)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('merchant:store_list'))

    context = {'form': form}
    return render(request, "edit_store.html", context)

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