from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Store
from .forms import StoreForm
from django.core import serializers
from product.models import Product


def store_list(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'store_list.html', context)

def get_stores(request):
    data = Store.objects.all()
    return HttpResponse(serializers.serialize("json", data), 
    content_type="application/json")

def add_store(request):
    form = StoreForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('merchant:store_list')

    context = {'form': form}
    return render(request, "add_store.html", context)

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