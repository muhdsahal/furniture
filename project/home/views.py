from django.shortcuts import render
from products.models import Product

# Create your views here.
def home(request):
    return render (request,'home.html')



def shop(request):
    product = Product.objects.all().order_by('id')
    return render (request,'shop.html',{'products':product})