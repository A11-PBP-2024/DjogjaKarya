from django.urls import path
from review import views  # Ubah ini
from review.views import get_reviews, add_review_api  # Ubah ini

app_name = 'review'

urlpatterns = [  # Pastikan ini didefinisikan sebagai list
    path('product/<int:product_id>/reviews/', views.review_list, name='review_list'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('api/reviews/', get_reviews, name='get_reviews'),
    path('api/reviews/add/', add_review_api, name='add_review_api'),
]