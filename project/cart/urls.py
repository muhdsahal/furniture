from .import views
from django.urls import path

urlpatterns = [ 
    path('',views.cart,name='cart'),
    path('add_cart',views.add_cart,name='add_cart'),
    path('delete-cart-item/', views.deletecartitem, name='deletecartitem'),
    path('update_cart/', views.update_cart, name='update_cart'),


]
