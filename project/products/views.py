from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product
from variant.models import Variant,Color
from categories.models import Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url='admin_login1')
def product (request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    product=Product.objects.filter(is_available=True).order_by('id')
    contex={
        'product':product,
        'Category': Category.objects.filter(is_available=True).order_by('id')
    }
    return render (request,'product/products.html',contex)


@login_required(login_url='admin_login1')
def addproduct(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    # product deatil
    if request.method == 'POST':
        name=request.POST.get('product_name')
        price=request.POST.get('product_price')
        category_id=request.POST.get('category')
        description=request.POST.get('product_description')
        
    
    
    #validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request,'product name already exists')
            return redirect('product')
        
        if name == '' or price =='':
            messages.error(request,'name or price is empty ')
            return redirect('product')
        
        price=int(price)
        if not price >= 0:
            messages.error(request,'positive numbers only!..')
            return redirect('product')
        
        if category_id:
            category=Category.objects.get(id=category_id)
        else:
            category = None

        # save
        product=Product(
            product_name=name,
            category=category,
            product_price=price,
            product_description=description,
        
        )
        product.save()
        messages.success(request,'Product Added Successfully')

        return redirect('product')
    
    return render(request,'product/products.html')

@login_required(login_url='admin_login1')
def product_delete(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    delete_product=Product.objects.get(id=product_id)
    variants=Variant.objects.filter(product=delete_product)
    for variant in variants:
        variant.is_available=False
        variant.quantity = 0 
        variant.save()
    delete_product.is_available = False
    delete_product.save()
    messages.success(request,'product deleted successfully')
    return redirect('product')


@login_required(login_url='admin_login1')
def product_edit(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    if request.method == 'POST':
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        category_id = request.POST.get('category')
        product_description = request.POST.get('product_description')
         
        if name.strip() == '' or price.strip() == '':
                messages.error(request, "Name or Price field are empty!")
                return redirect('product')
        
        price=int(price)
        if not price >=0:
            messages.error(request, 'positive numbers only!')
            return redirect('product')
        
        category_obj = Category.objects.get(id=category_id)

        
        if Product.objects.filter(product_name=name).exists():
             
            check = Product.objects.get(id=product_id)
            
            if name == check.product_name:
                pass
            else:
                messages.error(request, 'Product name already exists')
                return redirect('product')
                    
        editproduct= Product.objects.get(id=product_id)
        editproduct.product_name= name
        editproduct.product_price=price
        editproduct.category=category_obj
        editproduct.product_description=product_description
        editproduct.save()
        messages.success(request,'product edited successfully!')
        
        return redirect('product') 
    
def product_view(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    variant=Variant.objects.filter(product=product_id,is_available=True)
    color_name=Color.objects.all().order_by('id')
    product=Product.objects.all().order_by('id')
    variant_list={
        'variant':variant,
        'product':product,
        'color_name':color_name
    }
    return render(request,'adminside/product_view.html',{'variant_list':variant_list})
