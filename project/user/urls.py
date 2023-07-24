from django.urls import path
from .import views

urlpatterns = [
    path('user_signup',views.user_signup,name='user_signup'),
    path('home/user_login1',views.user_login1,name='user_login1'),
    path('logout1',views.logout1,name='logout1'),
    path('forgot_password',views.forgot_password,name='forgot_password'),

    
]   