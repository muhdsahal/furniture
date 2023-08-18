from django.urls import path
from .import views


urlpatterns = [
    # path('admin_signup',views.admin_signup,name='admin_signup'),
    path('usermanagement_1',views.usermanagment_1,name='usermanagement_1' ),
    path('admin_login1',views.admin_login1,name='admin_login1'),
    path('admin_logout1',views.admin_logout1,name='admin_logout1'),
    path('dashboard', views.dashboard, name='dashboard'),  
    path('blockuser/<int:user_id>',views.blockuser,name='blockuser'),
    # path('banner',views.banner,name='banner'),
    # path('createbanner',views.createbanner,name='createbanner')
    
   


]
