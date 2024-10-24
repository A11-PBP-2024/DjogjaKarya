from django.urls import path
from product.views import show_category, show_detail, filter_category_ajax

app_name = 'product'

urlpatterns = [
    # path('', coba, name='show_category'),
    path('detail/<int:id>', show_detail, name='show_detail'),
    path('', show_category, name='show_category'),
    path('filter-kategori/', filter_category_ajax, name='filter-category-ajax'),
]

