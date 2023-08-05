from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Wishlist
from products.models import Product
from django.http import JsonResponse

# Create your views here.
#wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def wishlist(request):
    wishlist=Wishlist.objects.filter(use=request.user)
    context={
        'wishlist':wishlist,
    }
    return render(request,'wishlist/wishlist.html',context)

#add wishlist
def add_wishlist(request):
    if request.mehod == 'POST':
        if request.user.is_authenticated:
            prod_id=request.POST.get('prod_id')
            product_check=Product.objects.get(id=prod_id)
            
            if product_check:
                if Wishlist.objects.filter(user=request.user,product=product_check)
                return JsonResponse({'status':"product already in wishlist"})
                
            else:
                Wishlist.objects.create(user=request.user,product=product_check)
                return JsonResponse({'status':'product added wishlist'})
        else:
            return JsonResponse({'status':"login and continue"})
    else:
        return JsonResponse("something went wrong ,reload page",safe=False)
    
#delete wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def deletewishlist(request):
    if request.method == "POST"  :
        product_id= int(request.POST.get(product_id))
        wishlist=Wishlist.objects.filter(user=request.user,product=product_id)
        if wishlist.exists():
            wishlist.delete()
    return redirect('wishlist') 

