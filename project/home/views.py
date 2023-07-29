from django.shortcuts import render
from products.models import *
from categories.models import *




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
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('id').filter(product_name__icontains=keyword)
            if products.exists():
                product_ids=products.values_list('id',flat=True)
                context={
                    'cate':Category.objects.all(),
                    'products': products,

                }
                return render(request,'shop.html',context)
            else:
                message='product not found !'
                return render(request,'shop.html',{'message':message})
        else:
            message='please enter a valid  search keyword'
            return render(request,'shop.html',{'message':message})
    else:
        return render(request,'404.html')


