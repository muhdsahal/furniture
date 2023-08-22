from django.urls import path
from . import views

urlpatterns=[
    
    path('order_list/',views.order_list,name='order_list'),
    path('order_view/<int:view_id>',views.order_view,name='order_view'),
    path('change_status/',views.change_status,name='change_status'),
    path('order_search/',views.order_search,name='order_search'),
    path('order_payment_sort/',views.order_payment_sort,name='order_payment_sort'),
    path('order_status_show/',views.order_status_show,name='order_status_show'),
    path('return_order/<int:return_id>',views.return_order,name='return_order'),
    path('order_cancel/<int:cancel_id>',views.order_cancel,name='order_cancel'),
  

]