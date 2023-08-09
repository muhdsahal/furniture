from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product
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
        image1=request.FILES.get('product_image1',None)
        image2=request.FILES.get('product_image2',None)
        image3=request.FILES.get('product_image3',None)
        quantity=request.POST.get('quantity')
        category_id=request.POST.get('category')
        description=request.POST.get('product_description','')
        print(description,'jhbbbbbbbbbbbbbbbbbbbbbbbb')
    
    
    #validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request,'product name already exists')
            return redirect('product')
        
        if name == '' or price =='':
            messages.error(request,'name or price is empty ')
            return redirect('product')
        
        if not image1:
            messages.error(request,'image not found')
            return redirect('product')
        
        if not image2:
            messages.error(request,'image not found')
            return redirect('product')
        
        if not image3:
            messages.error(request,'image not found')
            return redirect('product')
        
        if category_id:
            category=Category.objects.get(id=category_id)
        else:
            category = None

        # save
        product=Product(
            product_image1=image1,
            product_image2=image2,
            product_image3=image3,
            product_name=name,
            category=category,
            product_price=price,
            product_quantity=quantity,
            product_description=description,
        
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
    else:
        return redirect('product')


@login_required(login_url='admin_login1')
def editproduct(request,editproduct_id):
    product = get_object_or_404(Product, slug=editproduct_id)

    if not request.user.is_superuser:
        return redirect('admin_login')

    try:
        product = Product.objects.get(slug=editproduct_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('product')

    if request.method == 'POST':
        pname = request.POST.get('product_name')
        pprice = request.POST.get('product_price')
        pdescription = request.POST.get('product_description')
        category_id = request.POST.get('category')
        quantit = request.POST.get('quantity')
        try:
            # Use get_object_or_404 to handle missing category_id
            cates = get_object_or_404(Category, id=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'Category not found')
            return redirect('product')


        try:
            is_availables = request.POST.get('checkbox', False)
            if is_availables == 'on':
                is_availables = True
            else:
                is_availables = False
        except:
            is_availables = False

        if pname == '' or pprice == '':
            messages.error(request, 'Name or Price field is empty')
            return redirect('product')

        if Product.objects.filter(product_name=pname).exists():
            check = Product.objects.get(slug=editproduct_id)
            if pname != check.product_name:
                messages.error(request, 'Product name already exists')
                return redirect('product')

        cates = Category.objects.get(id=category_id)

        cat = Product.objects.get(slug=editproduct_id)
        cat.product_name = pname
        cat.quantity = quantit
        cat.product_price = pprice
        cat.is_available = is_availables
        cat.category = cates
        cat.product_description = pdescription
        cat.save()
        return redirect('product')
    else:
        # Pre-fill the form with the existing values
        dict_list = {
            'product': product,
            'category': Category.objects.all()
            
            
        }
        return render(request, 'product/edit_product.html', dict_list)