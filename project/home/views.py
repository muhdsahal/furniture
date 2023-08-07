from django.shortcuts import render,redirect
from products.models import *
from categories.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





# Create your views here.
def home(request):
    return render (request,'home.html')



def shop(request):
    product = Product.objects.all().order_by('id')
    cate=Category.objects.all()
    context={
        'products':product,
        'cate':cate,
        
    }
    return render (request,'shop.html',context)


def items(request):
    cat = Category.objects.all()
    product = Product.objects.all().order_by('id')
    context={
        'products':product,
        'cat':cat
    }
    return render(request,'categoryhome.html',context)

def cat_detail(request, id):
    product=Product.objects.select_related('category').filter(category__id=id)
    return render(request,'shop.html',{'products':product}) 
                  


def product_details(request,id):
    product=Product.objects.get(id=id)
    product_id = product.id
    return render(request,'productdetails.html',{'prod':product}) 

def search_product(request):
    keyword = request.GET.get('keyword', '')
    if not keyword:
        return redirect('shop')

    products = Product.objects.order_by('id').filter(product_name__icontains=keyword)
    if products.exists():
        product_ids = products.values_list('id', flat=True)
        context = {
            'cate': Category.objects.all(),
            'products': products,
        }
        return render(request, 'shop.html', context)
    else:
        message = 'Product not found!'
        return render(request, 'shop.html', {'message': message})


def product_list(request):
    products = Product.objects.all()

    sort_option = request.GET.get('sort', '')
    size_filter = request.GET.get('size_filter', '')

    if sort_option == 'atoz':
        products = products.order_by('product_name')
    elif sort_option == 'ztoa':
        products = products.order_by('-product_name')

    if size_filter == 'small':
        products = products.filter(size='Small')
    elif size_filter == 'medium':
        products = products.filter(size='Medium')
    elif size_filter == 'large':
        products = products.filter(size='Large')

    paginator = Paginator(products, per_page=10)  # Number of products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'shop.html', context)
