from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('increase/<int:item_id>/', views.cart_increase, name='cart_increase'),
    path('decrease/<int:item_id>/', views.cart_decrease, name='cart_decrease'),
    path('remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
]









