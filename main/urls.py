from django.urls import path
from main.views import show_main
from wishlist.views import show_wishlist
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('wishlist/', show_wishlist, name='show_wishlist'),
]
