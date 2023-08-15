from django.shortcuts import render,redirect
from .models import Category
from products.models import Product
from variant.models import Variant
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='admin_login1')
def categories (request):
    if not request.user.is_superuser:
        return redirect ('admin_login1')
    Category_data=Category.objects.all().order_by('id')
    return render(request,'category/category.html',{'Category': Category_data})


@login_required(login_url='admin_login1')
def createcategory(request):
    try:
        if not request.user.is_superuser:
            return redirect('admin_login1')
    

        if request.method == "POST":
            image = request.FILES.get('image', None)
            name = request.POST.get('categories')
            description = request.POST.get('categories_discription')

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
            messages.success(request,'Category added successfully !')
            return redirect('categories')
    except:
        return redirect('categories')
        

def deletecategory(request,deletecategory_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    cate=Category.objects.get(id=deletecategory_id)
    products = Product.objects.filter(category=cate)
    for product in products:
        product.is_available = False
        product.save()

    variants = Variant.objects.filter(product=product)
    for variant in variants:
        variant.is_available = False
        variant.quantity = 0
        variant.save()

    cate.is_available = False
    cate.save()
    messages.success(request,'category deleted successfully !.')
    return redirect ('categories')

# def blockcategory(request,cate_id):
#     if not request.user.is_superuser:
#         return redirect('admin_login1')
#     cate=Category.objects.filter(id=cate_id)
    
#     if cate.is_active:
#         cate.is_active=True
#         cate.save()
#     else:
#         cate.is_active =False
#         cate.save()
#         return redirect('categories')


@login_required(login_url='admin_login1')
def editcategory(request,editcategory_id):
    if not request.user.is_superuser:
        return redirect ('admin_login1')
    if request.method == 'POST':
        name=request.POST.get('categories')
        description=request.POST.get('categories_discription')


        try:
            cate=Category.objects.get(slug=editcategory_id)
            image=request.FILES.get('image')
            if image:
                cate.categories_image=image             
                cate.save()
        except Category.DoesNotExist:
            messages.error(request,'image not found')
            return redirect('categories')
        if name.strip()=='':
            messages.error(request,'Name field is empty')
            return redirect('categories')
        if Category.objects.filter(categories=name).exists():
            check=Category.objects.get(slug=editcategory_id)

            if name == check.categories:
                pass
            else:
                messages.error(request,'category images already exist !')
                return redirect('categories')
            
        cate=Category.objects.get(slug=editcategory_id)
        cate.categories = name
        cate.categories_description=description
        cate.save()
        return redirect('categories')
    # return redirect('categories')
