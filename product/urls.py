from django.urls import path
from product.views import show_category, show_detail, filter_category_ajax, add_product,get_product, edit_product, delete_product, get_product_id, get_form_data

app_name = 'product'

urlpatterns = [
    # path('', coba, name='show_category'),
    path('detail/<int:id>', show_detail, name='show_detail'),
    path('', show_category, name='show_category'),
    path('filter-kategori/', filter_category_ajax, name='filter-category-ajax'),
    path('add-product/', add_product, name='add_product'),
    path('json/', get_product, name='get_product'),
    path('edit/<int:id>/', edit_product, name='edit_product'),  # URL untuk edit produk
    path('delete/<int:id>/', delete_product, name='delete_product'),  # URL untuk delete produk
    path('product/<int:id>/', get_product_id, name='get_product_id'),
     path('get-form-data/', get_form_data, name='get_form_data'),
]

