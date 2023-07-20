from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product
from categories.models import Category
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='admin_login1')
def product (request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    product=Product.objects.all().order_by('id')
    return render (request,'product/products.html',{'product':product})


@login_required(login_url='admin_login1')
def addproduct(request):

    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    # product deatil
    if request.method == 'POST':
        name=request.POST.get('product_name')
        price=request.POST.get('product_price')
        image=request.FILES.get('product_image',None)
        quantity=request.POST.get('quantity')
        category_id=request.POST.get('category')
    
    
    #validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request,'product name already exists')
            return redirect('product')
        
        if name == '' or price =='':
            messages.error(request,'name or price is empty ')
            return redirect('product')
        
        if not image:
            messages.error(request,'image not found')
            return redirect('product')
        if category_id:
            category=Category.objects.get(id=category_id)
        else:
            category = None

        # save
        product=Product(
            product_image=image,
            product_name=name,
            category=category,
            product_price=price,
            product_quantity=quantity,
        
        )
        product.save()
        return redirect('product')
    return render(request,'product/products.html')

def deleteproduct(request,deleteproduct_slug):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    pro = Product.objects.get(slug=deleteproduct_slug)
    pro.delete()
    
    return redirect('product')
