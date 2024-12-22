from django.urls import path
from . import views

app_name = 'article'  # This is crucial for using the 'article' namespace

urlpatterns = [
    path('', views.show_article, name='show_article'),
    path('detail/<int:id>/', views.detail_blog, name='detail_blog'),
    path('add/', views.add_article, name='add_article'),
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('add-article-flutter/', views.add_article_flutter,
         name='add_article_flutter'),
    path('edit-article-flutter/<int:article_id>/',
         views.edit_article_flutter, name='edit_article_flutter'),
    path('delete-article-flutter/<int:article_id>/',
         views.delete_article_flutter, name='delete_article_flutter'),
    # Add more URL patterns here as needed
]
