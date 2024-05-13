from . import views
from django.urls import path


urlpatterns = [
    path('products/', views.shop_view, name="shop"),
    path('products/<str:selected_tags>', views.shop_view, name="filtered_product_list"),
    path('basket/', views.basket_view, name="basket"),
    path('checkout/', views.checkout_view, name="checkout"),
    path('product/add/', views.add_product, name="add_product"),
    path('product/add/<str:pk>/', views.edit_product, name="edit_product"),
    path('product/<str:pk>/', views.product_detail, name="product_detail"),
]
