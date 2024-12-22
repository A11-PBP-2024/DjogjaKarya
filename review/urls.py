from django.urls import path
from review import views  
from review.views import get_reviews, add_review_api, delete_review_api  

app_name = 'review'

urlpatterns = [ 
    path('product/<int:product_id>/reviews/', views.review_list, name='review_list'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('api/reviews/', get_reviews, name='get_reviews'),
    path('api/reviews/add/', add_review_api, name='add_review_api'),
    path('product/<int:product_id>/reviews/delete/<int:review_id>/', 
         views.delete_review, name='delete_review'),
    path('api/reviews/<int:review_id>/delete/', delete_review_api, name='delete_review_api'),
]