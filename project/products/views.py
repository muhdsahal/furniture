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
    contex={
        'product':product,
        'Category': Category.objects.all()
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
    try :
        product=Product.objects.get(slug=deleteproduct_slug)
    except Product.DoesNotExist:
        return redirect('product')
    product.product_quantity=0
    if product.is_available:
        product.is_available=False

    
    product.save()
    
    return redirect('product')


@login_required(login_url='admin_login1')
def editproduct(request,editproduct_id):
    if not request.is_superuser:
        return redirect('admin_login1')

    try:
        product=Product.objects.get(slug=editproduct_id)
    except Product.DoesNotExist:
        messages.error(request,'product not found')
        return redirect('product')
    
    if request.method == 'POST':
        pname=request.POST.get('product_name')
        pprrice=request.POST.get('product_price')
        pdiscription=request.POST.get('product_discription')
        category_id=request.POST.get('category')
        pquantity=request.POST.get('quantity')


        #validation 
        try:
            pro= Product.objects.get(slug=editproduct_id)
            image=request.FILES.get('product_image')
            if image:
                pro.product_image= image
                pro.save()

        except Product.DoesNotExist:
            messages.error(request,'product not found')
            return redirect ('product')
        
        try :
            is_available= request.POST.get('checkbox',False)
            if is_available == 'on':
                is_available = True
            else:
                is_available = False
        except:
            is_available = False

            if pname =='' or pprrice =='':
                messages.error(request,'name or price field is empty')
                return redirect ('product')
        
        if Product.objects.filter(product_name=pname).exists():
            check =Product.objects.get(slug=editproduct_id)
            if pname != check.product_name:
                messages.error(request,'product name already exist')
                return redirect ('product')
        cate=Category.objects.get(id=category_id)
        cat=Product.objects.get(slug=editproduct_id)
        cat.product_name = pname
        cat.product_quantity = pquantity
        cat.product_price = pprrice
        cat.product_discription = pdiscription
        cat.is_available = is_available
        cat.category = category_id
        cat.save()
        
        return redirect('product')
    else:
        dict_list={
            'product':product,
            'category':Category.objects.all(),

        }
        return render (request,'product/editproduct.html',dict_list)

    

