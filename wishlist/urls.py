from django.urls import path
from .views import show_wishlist, add_to_wishlist, remove_from_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('api/', show_wishlist, name='api_show_wishlist'),
    path('api/add/<int:product_id>/', add_to_wishlist, name='api_add_to_wishlist'),
    path('api/remove/<int:product_id>/', remove_from_wishlist, name='api_remove_from_wishlist'),
]
