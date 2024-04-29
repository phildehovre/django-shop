from . import views
from django.urls import path
from . import views



urlpatterns = [
    path('', views.account_view, name="account"),
    path('orders/', views.orders_view, name="orders"),
    path('orders/<str:order_id>', views.order_detail, name="order_detail"),
    path('settings/', views.settings_view, name="settings"),
]

