from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from variant.models import VariantImage
from .models import Wishlist
from django.http import HttpResponse
from products.models import Product
from django.http import JsonResponse

# Create your views here.
#wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def wishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    variants = wishlist.values_list('product', flat=True)
    img = VariantImage.objects.filter(variant__product__in=variants).distinct('variant')
    context={
        'wishlist':wishlist,
        'img':img,
    }
    return render(request,'wishlist/wishlist.html',context)

#add wishlist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Wishlist

def add_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('prod_id')
           
            product_check = get_object_or_404(Product, id=prod_id)
            
            if Wishlist.objects.filter(user=request.user, product=product_check).exists():
                return JsonResponse({'status': "product already in wishlist"})
            else:
                Wishlist.objects.create(user=request.user, product=product_check)
                return JsonResponse({'status': 'product added to wishlist'})
        else:
            return JsonResponse({'status': "login and continue"})
    else:
        return JsonResponse({'status': "something went wrong, reload page"}, status=400)

    
#delete wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def deletewishlist(request):
    if request.method == "POST"  :
        product_id = request.POST.get('product_id')
        wishlist=Wishlist.objects.filter(user=request.user,product=product_id)
        if wishlist.exists():
            wishlist.delete()
    return redirect('wishlist') 

