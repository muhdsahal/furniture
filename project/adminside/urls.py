from django.urls import path
from .import views


urlpatterns = [
    # path('admin_signup',views.admin_signup,name='admin_signup'),
    path('usermanagement_1',views.usermanagment_1,name='usermanagement_1' ),
    path('admin_login1',views.admin_login1,name='admin_login1'),
    path('admin_logout1',views.admin_logout1,name='admin_logout1'),
    path('dashboard', views.dashboard, name='dashboard'),  
    path('blockuser/<int:user_id>',views.blockuser,name='blockuser'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path('export_csv/',views.export_csv,name='export_csv'),
    path('generate_pdf/',views.generate_pdf,name='generate_pdf'),
    path('user_sort/',views.user_sort,name='user_sort'),
    path('user_block_status/',views.user_block_status,name='user_block_status'),
    
   


]
