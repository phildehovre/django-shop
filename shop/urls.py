from . import views
from django.urls import path

urlpatterns = [
    path('', views.shop_view, name="shop"),
    path('basket/', views.basket_view, name="basket"),
    path('<str:product_id>/', views.product_detail, name="product_detail"),
]
