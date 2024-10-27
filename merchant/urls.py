from django.urls import path
from merchant.views import store_list, add_store, edit_store, delete_store, get_stores,store_products

app_name = 'merchant'

urlpatterns = [
    path('', store_list, name='store_list'),
    path('get-stores/', get_stores, name='get_stores'),
    path('add/', add_store, name='add_store'),
    path('edit-store/<int:id>/', edit_store, name='edit_store'),
    path('delete/<int:id>', delete_store, name='delete_store'),
    path('products/', store_products, name='store_products'),

]
