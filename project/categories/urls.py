from django.urls import path
from .import views


urlpatterns = [
    path('',views.categories,name='categories'),
    path('createcategory/',views.cretecategory,name='createcategory')
]
