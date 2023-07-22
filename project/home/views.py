from django.shortcuts import render
from products.models import Product
from categories.models import Category


# Create your views here.
def home(request):
    return render (request,'home.html')



def shop(request):
    product = Product.objects.all().order_by('id')
    return render (request,'shop.html',{'products':product})


def items(request):
    category=Category.objects.all().order_by('id')
    return render(request,'categoryhome.html',{'categories':category})


def product_details(request,product_id):
    product=Product.objetcs.get(slug=product_id)

    related=Product.objects.order_by('?')[:5]
    return render(request,'productdetails.html',{'prod':product,'allpro':related}) 