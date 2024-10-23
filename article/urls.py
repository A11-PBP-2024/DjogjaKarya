from django.urls import path
from . import views

app_name = 'article'  # This is crucial for using the 'article' namespace

urlpatterns = [
    path('', views.show_article, name='show_article'),
    # Add more URL patterns here as needed
]
