from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

from products.models import Product
from django.http.response import JsonResponse
from cart.models import Cart

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id=request.POST.get('prod_id')

            try:
                product_check=Product.objects.get(id=prod_id)
            
            except Product.DoesNotExist:
                return JsonResponse({'status':'no such product found '})
            
            if Cart.objects.filter(user=request.user,product_id=prod_id).exists():
                return JsonResponse({'status':'Product already in cart'})
            else:
                prod_qty=int(request.POST.get('product_qty'))
        else:
            return JsonResponse({'status':'login to continue'})
    return redirect('product_details')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def cart(request):
    cart=Cart.objects.filter(user=request.user).order_by('id')
    total_price=0
    tax=0
    grand_total=0
    single_product_total=[0]
    for item in cart:
        total_price = total_price + item.prodcut.product_price * item.product_qty
        single_product_total.append(item.prodcut.product_price * item.product_qty)
        tax =total_price * 0.18
        grand_total = total_price + tax
    

    context={
        'cart':cart,
        'total_price':total_price,
        'tax':tax,
        'grand_total':grand_total,
        'single_product_total':single_product_total,
    }
    return render(request,'cart/cart.html',context)


