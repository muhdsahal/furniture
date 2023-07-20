from django.urls import path
from .import views

urlpatterns = [
    path('product',views.product,name='product'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('deleteproduct/<slu:deleteproduct_slug>',views.deleteproduct,name='deleteproduct'),
]
