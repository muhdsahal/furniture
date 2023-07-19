from django.shortcuts import render,redirect
from .models import Category
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='admin_login1')
def categories (request):
    if not request.user.is_superuser:
        return redirect ('admin_login')
    Category_data=Category.objects.all().order_by('id')
    return render(request,'category/category.html',{'Category': Category_data})


@login_required(login_url='admin_login1')
def cretecategory(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    

    if request.method == "POST":
        image = request.FILES.get('image', None)
        name = request.POST['categories']
        description = request.POST['categories_discription']

        # Validation
        if name.strip() == '':
            messages.error(request, 'Name not found')
            return redirect('categories')

        if not image:
            messages.error(request, 'Image not uploaded')
            return redirect('categories')

        if Category.objects.filter(categories=name).exists():
            messages.error(request, 'Category name already exists')
            return redirect('categories')

        category_instance = Category(categories=name, categories_description=description, categories_image=image)
        category_instance.save()
         
        return redirect('categories')

