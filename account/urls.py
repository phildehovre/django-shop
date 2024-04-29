from . import views
from django.urls import path
from . import views



urlpatterns = [
    path('', views.account_view, name="account"),
    path('orders/', views.orders_view, name="orders"),
    path('orders/<str:order_id>', views.order_detail, name="order_detail"),
    path('settings/', views.settings_view, name="settings"),
    path('payments/', views.payment_methods, name="payment_methods"),
    path('delete_address/<str:pk>/', views.delete_address, name="delete_address"),
]

