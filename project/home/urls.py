from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('shop',views.shop,name='shop'),
    path('items',views.items,name='items'),
    path('product_details',views.product_details,name='product_details'),


]