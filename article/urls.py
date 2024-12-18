from django.urls import path
from . import views

app_name = 'article'  # This is crucial for using the 'article' namespace

urlpatterns = [
    path('', views.show_article, name='show_article'),
    path('detail/<int:id>/', views.detail_blog, name='detail_blog'),
    path('add/', views.add_article, name='add_article'),
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
    # Add more URL patterns here as needed
]
