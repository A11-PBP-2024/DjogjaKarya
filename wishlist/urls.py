from django.urls import path
from wishlist.views import show_wishlist, add_to_wishlist, remove_from_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
