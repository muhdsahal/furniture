from .import views
from django.urls import path

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart',views.add_cart,name='add_cart'),
]
