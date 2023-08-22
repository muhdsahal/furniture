from django.urls import path
from . import views

urlpatterns=[
    
    path('coupon/',views.coupon,name='coupon'),
    path('add_coupon/',views.add_coupon,name='add_coupon'),
    path('coupon_search/',views.coupon_search,name='coupon_search'),
    path('edit_coupon/<int:coupon_id>',views.edit_coupon,name='edit_coupon'),
    path('delete_coupon/<int:coupon_id>',views.delete_coupon,name='delete_coupon'),
   
]