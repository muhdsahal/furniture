from django.urls import path
from .import views


urlpatterns = [
    path('',views.categories,name='categories'),
    path('createcategory',views.createcategory,name='createcategory'),
    path('deletecategory/<slug:deletecategory_id>',views.deletecategory,name='deletecategory'),
    path('editcategory/<slug:editcategory_id>',views.editcategory,name='editcategory'),
]
