
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('about/', views.about_view, name="about"),
    path('login/', views.login_view, name='login_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
]
