from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
]
