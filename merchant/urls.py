from django.urls import path
from merchant.views import store_list, show_xml, show_json, add_store, edit_store, delete_store

app_name = 'merchant'

urlpatterns = [
    path('store-list/', store_list, name='store_list'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('add/', add_store, name='add_store'),
    path('edit-store/<uuid:id>', edit_store, name='edit_store'),
    path('delete/<uuid:id>', delete_store, name='delete_store'),
]
