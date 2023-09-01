from django.shortcuts import render,redirect
from products.models import *
from categories.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from variant.models import VariantImage,Variant
from django.template.loader import render_to_string
from banner.models import banner




# Create your views here.
def home(request):  
    cate=Category.objects.all()
    banners =banner.objects.all()
    context={
       'cate' :cate,
       'banners':banners,
    
   }

    return render (request,'home.html',context)




def shop(request):
    if request.user.is_superuser:
        return  redirect('dashboard')
    
    
    product = Product.objects.filter(is_available=True).order_by('id')
    cate=Category.objects.filter(is_available=True)
    variant_images = VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
    paginator =Paginator(product,3)
    page =request.GET.get('page')
    paged_products= paginator.get_page(page)
    product_count =product.count()
    context={
        'product':paged_products,
        'cate':cate,
        'variant_images':variant_images,
        'product_count':product_count
        
    }

    return render (request,'shop.html',context)





def items(request):
    cat = Category.objects.all()
    product = Product.objects.filter(is_available=True).order_by('id')
    variant_images = VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
   

    context={
        'products':product,
        'cat':cat,
        'variant_images':variant_images
        
    }
    return render(request,'categoryhome.html',context)

def cat_detail(request, cate_id):
    categories=Category.objects.get(id=cate_id)

    
    
    variant_images = VariantImage.objects.filter(variant__product__category__id=cate_id,is_available=True).order_by('variant__product').distinct('variant__product')
    context={
    
        'variant_images':variant_images,
        'categories':categories
    }
   
    return render(request,'shop.html',context)

                  


def product_details(request,prod_id,img_id):
    
    product=Product.objects.get(id=prod_id)
    product_id = product
    variant = VariantImage.objects.filter(variant=img_id,is_available=True)
    variant_images = VariantImage.objects.filter(variant__product__id=prod_id,is_available=True).distinct('variant__product')
    color=VariantImage.objects.filter(variant__product__id=prod_id,is_available=True).distinct('variant__color')
    context={
        'prod':product_id,
        'variant_images':variant_images,
        'variant':variant,
        'color':color
    }
    return render(request,'productdetails.html',context) 

def search_product(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            variant_images = VariantImage.objects.filter(variant__product__product_name__icontains=keyword,is_available=True).order_by('variant__product').distinct('variant__product')
            if variant_images.exists():
                context = {
                    'cate': Category.objects.all(),
                    'variant_images': variant_images,
                }
                return render(request, 'shop.html', context)
            else:
                context = {
                    'cate': Category.objects.all(),

                }
                messages.error(request, 'search not found! ') 
                return render(request, 'shop.html', context)
        else:
            messages.error(request, 'Please enter a valid search keyword') 
            return render(request, 'shop.html')
    else:
        return render(request, '404.html')



def product_list(request):
    if request.user.is_superuser:
        return redirect('dashboard')

    sort_option = request.GET.get('sort')
    products = Product.objects.filter(is_available=True)
    cat = Category.objects.all()

    if sort_option == 'atoz':
        sorted_products = products.order_by('product_name')
    elif sort_option == 'ztoa':
        sorted_products = products.order_by('-product_name')
    elif sort_option == 'lowtohigh':
        sorted_products = products.order_by('product_price')
    elif sort_option == 'hightolow':
        sorted_products = products.order_by('-product_price')
    else:
        sorted_products = products

    items_per_page = 4
    paginator = Paginator(sorted_products, items_per_page)
    page_number = request.GET.get('page')

    try:
        products_page = paginator.page(page_number)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    return render(request, 'shop.html', {'sorted_products': sorted_products, 'cat': cat, 'products_page': products_page})




def product_sort(request, sort_id):
    sort_option = sort_id
    base_query = VariantImage.objects.filter(variant__product__is_available=True)

    if sort_option == 1:
        variant_images = base_query.order_by('variant__product').distinct('variant__product')
    elif sort_option == 2:
        variant_images = base_query.order_by('variant__product__product_name').distinct('variant__product__product_name')
    elif sort_option == 3:
        variant_images = base_query.order_by('-variant__product__product_name').distinct('variant__product__product_name')
    elif sort_option == 4:
        variant_images = base_query.order_by('variant__product__product_price').distinct('variant__product__product_price')
    elif sort_option == 5:
        variant_images = base_query.order_by('-variant__product__product_price').distinct('variant__product__product_price')
    elif sort_option == 6:
        variant_images = base_query.filter(variant__product__offer__isnull=False).distinct('variant__product__id')


        
    products = Product.objects.filter(is_available=True).order_by('id')
    categories = Category.objects.all()

    context = {
        'products': products,
        'cate': categories,
        'variant_images': variant_images
    }

    return render(request, 'shop.html', context)
