from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Store
from .forms import StoreForm
from django.core import serializers


def store_list(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'store_list.html', context)

def show_xml(request):
    data = Store.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Store.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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
