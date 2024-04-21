from . import views
from django.urls import path

urlpatterns = [
    path('', views.shop_view, name="shop"),
    path('<str:product_id>/', views.product_detail, name="product_detail"),
]
