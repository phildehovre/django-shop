
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.base_view, name="home"),
    path('about/', views.about_view, name="about"),
    path('login/', views.login_view, name='login_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('account/',include('account.urls'), name="account_urls"),
    path("accounts/", include("django.contrib.auth.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)