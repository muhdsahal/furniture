from django.shortcuts import render
from products.models import *
from categories.models import *




# Create your views here.
def home(request):
    return render (request,'home.html')



def shop(request):
    product = Product.objects.all().order_by('id')
    context={
        'products':product,
        
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