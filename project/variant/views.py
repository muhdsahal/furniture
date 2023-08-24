from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Product,Variant,VariantImage,Color
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import webcolors
from django.http import JsonResponse
from .forms import ImageForm
from categories.models import Category
# Create your views here.
def  product_variant(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    variant =Variant.objects.filter(is_available=True).order_by('id')
    color_name = Color.objects.filter(is_available=True).order_by('id')
    product = Product.objects.filter(is_available=True).order_by('id')
    variant_list={
        'variant' :variant,
        'color_name':color_name,
        'product':product,
    }
    return render(request,'adminside/variant.html',{'variant_list':variant_list})  


def add_Product_Variant(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    if request.method == 'POST':
        variant_name =request.POST.get('variant_name')
        variant_color =request.POST.get('variant_color')
        variant_quantity =request.POST.get('variant_quantity')
    
    if variant_quantity.strip() == '':
        messages.error(request,'Quantity field is empty !')
        return redirect('product_variant')
    
    variant_quantity=int(variant_quantity)
    if not variant_quantity >=0:
        messages.error(request,'positive numbers only !.')
        return redirect('product_variant')
    

        
    
    try:
        product_obj = Product.objects.get(id=variant_name)
        color_obj = Color.objects.get(id=variant_color)

        if Variant.objects.filter(product=product_obj,color=color_obj).exists():
            messages.error(request,'Variant with the same product,color already exist !')
            return redirect('product_variant')
        
        add_variant= Variant(
            product=product_obj,
            color=color_obj,
            quantity=variant_quantity,
        )
        add_variant.save()

        messages.success(request,'variant added successfully ')
        return redirect('product_variant')
    except ObjectDoesNotExist:
        messages.error(request,'Invalid product ,color  selected')
        return redirect('product_variant')
    
    
    return render(request,'adminside/variant.html')

def edit_prodectvariant(request,variant_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    if request.method == 'POST':
        variant_name =request.POST.get('variant_name')
        variant_color =request.POST.get('variant_color')
        variant_quantity =request.POST.get('variant_quantity')

        if variant_quantity.strip() == '':
            messages.error(request,'quantity filed is empty !')
            return redirect('product_variant')
        
        variant_quantity=int(variant_quantity)
        if not variant_quantity >= 0:
            messages.error(request,'positve numbers only!')
            return redirect('product_variant')
    

        product_obj = Product.objects.get(id=variant_name)
        color_obj = Color.objects.get(id=variant_color)

        if Variant.objects.filter(product=product_obj,color=color_obj).exists():
            check =Variant.objects.get(id=variant_id)
            if product_obj == check.product and color_obj == check.color:
                pass
            else:
                messages.error(request,'Variant with the same product,color is already exist!')
                return redirect('product_variant')
            
        edit_variant=Variant.objects.get(id=variant_id)
        edit_variant.color=color_obj
        edit_variant.product=product_obj
        edit_variant.quantity=variant_quantity 
        edit_variant.save()
        messages.success(request,'product edited successfully')

        return redirect('product_variant')
    
def prodectvariant_delete(request, variant_id):
    if not request.user.is_superuser:   
        return redirect('admin_login1')
    delete_productvariant = Variant.objects.get(id=variant_id)
    print(delete_productvariant,id,'oooooooooooooooooooo')
    delete_productvariant.is_available=False
    delete_productvariant.quantity=0
    delete_productvariant.save()
    # delete_productvariant(is_available=True)
    messages.success(request,'product variant deleted successfully!')
    return redirect('product_variant')

def product_color(request):
    if not request.user.is_superuser:
            return redirect('admin_login1')
    product_color= Color.objects.filter(is_available=True).order_by('id')
    return render(request,'adminside/color_management.html',{'products_color':product_color})

def add_color(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    if request.method == 'POST':
        colorname = request.POST.get('color1')
        color = request.POST.get('color')
        color1 = color
        
        color = get_color_name(color)
        if color == 'Unknown':
            color = color1

        if colorname.strip() == '':
            messages.error(request, 'Field cannot be empty!')
            return redirect('product_color')

        if Color.objects.filter(color_name=colorname).exists():
            messages.error(request, 'Color already exists!')
            return redirect('product_color')

        color_object = Color(color_name=colorname, color_code=color)
        color_object.save()
        
        messages.success(request, 'Color added successfully!')
        return redirect('product_color')

    return render(request, 'adminside/color_management.html')

def color_delete(request,color_name_id):
     if not request.user.is_superuser:
        return redirect('admin_login1')
     delete_color=Color.objects.get(id=color_name_id)
     delete_color.is_available=False
     delete_color.save()
     messages.success(request,'color delete successfully !')
     
     return redirect('product_color')

def get_color_name(color_code):
    try:
        color_name = webcolors.rgb_to_name(webcolors.hex_to_rgb(color_code))
        return color_name
    except ValueError:
        return "Unknown"

def image_list(request,variant_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    image=VariantImage.objects.filter(variant=variant_id,is_available =True)
    add_image = variant_id
    return render(request,'adminside/image_management.html',{'image':image,'add_image':add_image})

def image_view(request,img_id):
    if request.method == 'POST':
        form =ImageForm(request.POST,request.FILES)
        var = Variant.objects.get(id=img_id)
    
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.variant = var
            image_instance.save()
            print('image saved successfully')

            return JsonResponse({'message':'works','img_id':img_id})
        else:
            print('Form is not valid !',form.errors)
    else:
        form =ImageForm()
    context ={'form':form,'img_id':img_id}
    return render(request, 'adminside/image_add.html', context)

def image_delete(request,image_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    try:
        delete_image=VariantImage.objects.get(id=image_id)
        var_id =delete_image.variant.id
        delete_image=is_available=False
        delete_image.save()
        messages.success(request,'image deleted successfully')
        image = VariantImage.objects.filter(variant=var_id)
        add_image = var_id
        return render(request,'adminside/image_management.html',{'image':image,'add_image':add_image})
    except:
        return redirect ('product_variant')
    
def product_view(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    variant=VariantImage.objects.filter(variant__product=product_id ,is_available=True)
    color_name= Color.objects.filter(is_available=True).order_by('id')
    product=Product.objects.filter(is_available=True).order_by('id')
    variant_list={
        'variant'    :variant,
        'color_name' :color_name, 
         'product'   :product,
    }
    # variant_id
    return render(request,'adminside/variant_view.html',{'variant_list':variant_list}) 

def variant_search(request):
    search = request.POST.get('search')
    if search is None or search.strip() == '':
        messages.error(request,'Filed cannot empty!')
        return redirect('product_variant')
    variant = Variant.objects.filter( Q(product__product_name__icontains=search) 
                                     | Q(color__color_name__icontains=search) 
                                     | Q(quantity__icontains=search), is_available=True) 
    color_name = Color.objects.filter(is_available=True).order_by('id')
    product = Product.objects.filter(is_available=True).order_by('id')
    variant_list = {
        'variant'    :variant,
        'color_name' :color_name, 
         'product'   :product,
    }
    if variant :
        pass
        return render(request,'adminside/variant.html',{'variant_list':variant_list}) 
    else:
        variant:False
        messages.error(request,'Search not found!')
        return redirect('product_variant')    
       
    

        

