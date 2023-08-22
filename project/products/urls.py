from django.urls import path
from .import views

urlpatterns = [
    path('product',views.product,name='product'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('product_delete/<int:product_id>', views.product_delete, name='product_delete'),
    path('product_edit/<int:product_id>', views.product_edit, name='product_edit'),
    path('product_view/<int:product_id>', views.product_view, name='product_view'), 
    path('product_search/', views.product_search, name='product_search'),


]
