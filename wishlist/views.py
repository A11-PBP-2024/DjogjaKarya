from django.shortcuts import render

# Create your views here.
def show_wishlist(request):
    context = {"user": request.user}
    return render(request, "wishlist.html", context)