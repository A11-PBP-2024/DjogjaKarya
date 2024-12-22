from django.urls import path
from .views import show_wishlist, add_to_wishlist, remove_from_wishlist, show_wishlist_flutter, add_to_wishlist_flutter, remove_from_wishlist_flutter

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    path('api/', show_wishlist_flutter, name='api_show_wishlist_flutter'),
    path('api/add/<int:product_id>/', add_to_wishlist_flutter, name='api_add_to_wishlist'),
    path('api/remove/<int:product_id>/', remove_from_wishlist_flutter, name='api_remove_from_wishlist'),
]