from django.contrib import admin
from django.urls import path
from django.conf import settings
from .import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('shop',views.shop,name='shop'),
    path('items',views.items,name='items'),
    path('cat_detail/<int:cate_id>',views.cat_detail,name='cat_detail'),
    # path('product_details/<int:prod_id>/<int:img_id>/',views.product_details,name='product_details'),
    path('product_details/<int:prod_id>/<int:img_id>/', views.product_details, name='product_details'),
    path('search_product/',views.search_product,name='search_product'),
    path('product_list/',views.product_list,name='product_list'),
    path('product_sort/<int:sort_id>',views.product_sort,name='product_sort')



]