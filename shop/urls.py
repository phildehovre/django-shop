from . import views
from django.urls import path


urlpatterns = [
    path('products/', views.shop_view, name="shop"),
    path('products/<str:selected_tags>', views.shop_view, name="filtered_product_list"),
    path('basket/', views.basket_view, name="basket"),
    path('product/<str:product_id>/', views.product_detail, name="product_detail"),
]
