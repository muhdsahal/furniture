from django.shortcuts import render,redirect
from products.models import *
from categories.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from variant.models import VariantImage,Variant
from django.template.loader import render_to_string





# Create your views here.
def home(request):
    return render (request,'home.html')



def shop(request):
    product = Product.objects.filter(is_available=True).order_by('id')
    cate=Category.objects.all()
    variant_images = VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
    context={
        'products':product,
        'cate':cate,
        'variant_images':variant_images
        
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

def cat_detail(request, id):
    product=Product.objects.select_related('category').filter(category__id=id)
    variant_images = VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
    context={
        'products':product,
        'variant_images':variant_images
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
            products = Product.objects.order_by('id').filter(product_name__icontains=keyword)
            if products.exists():
                context = {
                    'cate': Category.objects.all(),
                    'products': products,
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



# def product_list(request):
#     products = Product.objects.filter(is_available=True)

#     sort_option = request.GET.get('sort', '')
#     size_filter = request.GET.get('size_filter', '')

#     if sort_option == 'atoz':
#         products = products.order_by('product_name')
#     elif sort_option == 'ztoa':
#         products = products.order_by('-product_name')

#     if size_filter == 'small':
#         products = products.filter(size='Small')
#     elif size_filter == 'medium':
#         products = products.filter(size='Medium')
#     elif size_filter == 'large':
#         products = products.filter(size='Large')

#     paginator = Paginator(products, per_page=9)  # Number of products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj
#     }
#     return render(request, 'shop.html', context)



def product_list(request):
    # Your existing code for filtering and sorting
    products = Product.objects.filter(is_available=True)

    sort_option = request.GET.get('sort', '')
    size_filter = request.GET.get('size_filter', '')

    if sort_option == 'atoz':
        products = products.order_by('product_name')
    elif sort_option == 'ztoa':
        products = products.order_by('-product_name')


    paginator = Paginator(products, per_page=9)  # Number of products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        # If it's an AJAX request, return a JSON response with the paginated content
        products_html = render_to_string('product_list_partial.html', {'page_obj': page_obj})
        return JsonResponse({'products_html': products_html})

    context = {
        'page_obj': page_obj
    }
    return render(request, 'shop.html', context)