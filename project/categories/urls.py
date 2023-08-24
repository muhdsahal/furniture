from django.urls import path
from .import views


urlpatterns = [
    path('',views.categories,name='categories'),
    path('createcategory',views.createcategory,name='createcategory'),
    path('deletecategory/<slug:deletecategory_id>',views.deletecategory,name='deletecategory'),
    path('image_views/<int:img_id>',views.image_views,name='image_views'),
    path('editcategory/<slug:editcategory_id>',views.editcategory,name='editcategory'),
    path('category_search/', views.category_search, name='category_search'),
 
]
