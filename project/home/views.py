from django.shortcuts import render
from products.models import Product
from categories.models import Category
from django.shortcuts import get_object_or_404




# Create your views here.
def home(request):
    return render (request,'home.html')



def shop(request):
    product = Product.objects.filter(is_available=True).order_by('id')
    return render (request,'shop.html',{'products':product})


def items(request):
    category=Category.objects.all().order_by('id')
    return render(request,'categoryhome.html',{'categories':category})

def product_details(request,product_id):
    product = get_object_or_404(Product, id=product_id)

    product=Product.objects.get(id=product_id)

    related=Product.objects.order_by('?')[:5]
    product_id = product.id
    return render(request,'home/productdetails.html',{'prod':product,'allpro':related}) 