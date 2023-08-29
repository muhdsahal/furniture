from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from variant.models import VariantImage
from wishlist.models import Wishlist
from products.models import Product
from variant.models import Variant
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
               
                product_check =Variant.objects.get(id=prod_id)
                
            except Product.DoesNotExist:
                return JsonResponse({'status':'No such prodcut found '})
            
            if Cart.objects.filter(user=request.user,variant=prod_id).exists():
               
                
                return JsonResponse({'status':'Product already in cart'})
                
            else:
                prod_qty=int(request.POST.get('product_qty'))
             
                if product_check.quantity>=prod_qty:
                    Cart.objects.create(user=request.user,variant=product_check,product_qty=prod_qty)
                    try:
                        if Wishlist.objects.filter(user=request.user,variant=prod_id,product_qty=prod_qty):
                            wishlist = Wishlist.objects.filter(user=request.user,variant=prod_id,product_qty=prod_qty)
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
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user).order_by('id')
        variants = cart.values_list('variant', flat=True)
        img = VariantImage.objects.filter(variant__in=variants).distinct('variant')

        total_price= 0
        tax= 0
        grand_total= 0
        single_product_total= 0
        offer_total_price = 0
        single_total_offer= 0
        for item in cart:
            if item.variant.product.offer:
                total_price = total_price + item.variant.product.product_price * item.product_qty
                offer_total_price = offer_total_price + item.variant.product.offer.discount_amount * item.product_qty
                single_product_total+item.variant.product.product_price * item.product_qty
                single_total_offer =single_total_offer+item.variant.product.offer.discount_amount * item.product_qty
                tax =total_price * 0.18
                grand_total = total_price + tax
            else:
                total_price = total_price + item.variant.product.product_price * item.product_qty
                single_product_total+item.variant.product.product_price * item.product_qty
                tax =total_price * 0.18
                grand_total = total_price + tax

            single_product_total =single_product_total-single_total_offer
            total_price=total_price-offer_total_price
            grand_total = total_price + tax
        
            

        context={
            'img':img,
            'cart':cart,
            'total_price':total_price,
            'tax':tax,
            'grand_total':grand_total,
            'single_product_total':single_product_total,
        }
        return render(request,'cart/cart.html',context)
    else:
        return render(request,'cart/cart.html')





@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('variant_id')
        print(product_id,'rrrrrrrrrrrrrrrrrr')
        if (Cart.objects.filter(user=request.user, variant=product_id)):
            prod_qty = int (request.POST.get('product_qty'))
            cart = Cart.objects.get(variant=product_id, user=request.user)
            cartes = cart.variant.quantity
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                if cart.variant.product.offer:
                    offer_price =prod_qty*cart.variant.product.offer.discount_amount
                    print(offer_price,'000000000000000000')
                    single=prod_qty*cart.variant.product.product_price
                    single =single-offer_price
                    cart.single_total = single
                else:    
                    single=cart.single_total =prod_qty*cart.variant.product.product_price
                cart.save()
               

                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
                offer_price = 0
                for item in carts:
                    if item.variant.product.offer:
                        total_price = total_price + item.variant.product.product_price * item.product_qty
                        offer_price = item.variant.product.offer.discount_amount * item.product_qty
                        total_price =total_price-offer_price
                    else:
                        total_price = total_price + item.variant.product.product_price * item.product_qty
                    
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,'product_price':cart.variant.product.product_price,'quantity':prod_qty})
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def deletecartitem(request):
    if request.method == 'POST':
        try:
            product_id = int(request.POST.get('product_id'))
            cart_items = Cart.objects.filter(user=request.user, variant=product_id)
            cart_items.delete()
        except ValueError:
            return HttpResponseBadRequest("Invalid product ID")  
        
    return redirect('cart')