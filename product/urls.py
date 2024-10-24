from django.urls import path
from product.views import show_product, show_category,show_detail, filter_category_ajax, show_coba

app_name = 'product'

urlpatterns = [
    # path('', coba, name='show_category'),
    path('detail/<int:id>', show_detail, name='show_detail'),
    path('', show_coba, name='show_category'),
    path('filter-kategori/', filter_category_ajax, name='filter-category-ajax'),
]