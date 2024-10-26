from django.urls import path
from . import views

app_name = 'article'  # This is crucial for using the 'article' namespace

urlpatterns = [
    path('', views.show_article, name='show_article'),
    path('detail/', views.blog_detail, name='blog_detail'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
    # Add more URL patterns here as needed
]
