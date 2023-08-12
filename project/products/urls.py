from django.urls import path
from .import views

urlpatterns = [
    path('product',views.product,name='product'),
    path('addproduct',views.addproduct,name='addproduct'),
    #path('delete/<slug:deleteproduct_slug>/', views.deleteproduct, name='deleteproduct'),
    # path('products/delete/<str:deleteproduct_slug>/', views.deleteproduct, name='deleteproduct'),
    path('product_delete/<int:product_id>', views.product_delete, name='product_delete'),
    # path('editproduct/<slug:editproduct_id>', views.editproduct, name='editproduct'),
    path('product_edit/<int:product_id>', views.product_edit, name='product_edit'),
    path('product_view/<int:product_id>', views.product_view, name='product_view'), 


]
