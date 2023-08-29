from django.urls import path
from . import views

urlpatterns=[
    
    path('banners/',views.banners,name='banners'),
    path('add_banners/',views.add_banners,name='add_banners'),
    path('edit_banner/<int:edit_banner_id>',views.edit_banner,name='edit_banner'),
    path('delete_banner/<int:delete_banner_id>',views.delete_banner,name='delete_banner'),
   
]





   