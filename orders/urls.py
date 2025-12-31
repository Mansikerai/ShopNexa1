from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('dummy-payment/', views.dummy_payment, name='dummy_payment'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
]