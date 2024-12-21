from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('product/<int:product_id>/reviews/', views.review_list, name='review_list'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
]
