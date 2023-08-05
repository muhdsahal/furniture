from  django.urls import path
from .import views

urlpatterns = [
    path('',views.profile,name='profile'),
    path('addaddress/',views.addaddress,name='addaddress'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('deleteaddress/<int:delete_id>',views.deleteaddress,name='deleteaddress'),
]
