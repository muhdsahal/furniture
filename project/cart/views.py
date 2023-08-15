from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from products.models import Product
from django.http.response import JsonResponse
from django.http import HttpResponseBadRequest
from cart.models import Cart


# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id=request.POST.get('prod_id')
            print(prod_id,'daxooo')

            try:
                product_check=Product.objects.get(id=prod_id)
            
            except Product.DoesNotExist:
                return JsonResponse({'status':'No such prodcut found '})
            
            if Cart.objects.filter(user=request.user,product_id=prod_id).exists():
                print(prod_id,'0111111111111111000000000001')
                
                return JsonResponse({'status':'Product already in cart'})
                
            else:
                prod_qty=int(request.POST.get('product_qty'))
                if product_check.product_quantity>=prod_qty:
                    Cart.objects.create(user=request.user,product_id=prod_id,product_qty=prod_qty)
                    try:
                        if Wishlist.objects.filter(user=request.user,product_id=prod_id,product_qty=prod_qty):
                            wishlist = Wishlist.objects.filter(user=request.user,product_id=prod_id,product_qty=prod_qty)
                            wishlist.delete()
                    except:
                        pass
                    return JsonResponse({'status':'Product added successfully'})
                else:
                    return JsonResponse({'status':'Only few quantity available'})
        else:
            return JsonResponse({'status':'you are not login please Login to continue'})
    return redirect('user_login1')
            
                
    


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def cart(request):
    cart=Cart.objects.filter(user=request.user).order_by('id')
    total_price=0
    tax=0
    grand_total=0
    single_product_total=[0]
    for item in cart:
        total_price = total_price + item.product.product_price * item.product_qty
        single_product_total.append(item.product.product_price * item.product_qty)
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




@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('variant_id')
        if (Cart.objects.filter(user=request.user, product=product_id)):
            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(product=product_id, user=request.user)
            cartes = cart.product.product_quantity
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                cart.save()
               

                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
                for item in carts:
                    
                    total_price = total_price + item.product.product_price * item.product_qty
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,'product_price':cart.product.product_price,'quantity':prod_qty})
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def deletecartitem(request):
    if request.method == 'POST':
        try:
            product_id = int(request.POST.get('product_id'))
            cart_items = Cart.objects.filter(user=request.user, product__id=product_id)
            cart_items.delete()
        except ValueError:
            return HttpResponseBadRequest("Invalid product ID")  
        
    return redirect('cart')