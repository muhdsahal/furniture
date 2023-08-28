from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.models import Cart
from coupon.models import Coupon
from wishlist.models import Wishlist
from userprofile.models import Address
# from django.contrib.auth.models import User
from django.contrib import messages
from products.models import *
from checkout.models import Order, OrderItem,Itemstatus,Orderstatus
from django.shortcuts import render, redirect
from variant.models import Variant,VariantImage
import random
import string
import re

def checkout(request):
    request.session['coupon_session'] = 0
    request.session['coupon_id']= None
    
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        print(coupon,'444444444444444444444444')
        if coupon is None:
            messages.error(request, 'coupon field is cannot empty!')
            return redirect('checkout')
        try:
            check_coupons =Coupon.objects.filter(coupon_code=coupon).first()
            print(check_coupons.coupon_discount_amount,'999999999999999999999')
            cartitems= Cart.objects.filter(user=request.user)
            total_price = 0
            grand_total = 0
            offer_price = 0
            tax = 0
            offer_price_total= 0
            all_offer = 0
            for item in cartitems:
                if item.variant.product.offer:
                    product_price = item.variant.product.product_price
                    total_price += product_price * item.product_qty
                    offer_price = item.variant.product.offer.discount_amount
                    offer_price_total = offer_price * item.product_qty
                    total_price = total_price - offer_price_total
                    all_offer = all_offer + offer_price_total
                    tax = total_price * 0.18
                    print(total_price,'000000000000000000000')
                    
                else:
                    product_price = item.variant.product.product_price
                    total_price += product_price * item.product_qty
                    tax = total_price * 0.18

            grand_total=total_price + tax
            if coupon:                                             
                if grand_total >= check_coupons.min_price:
                    request.session['coupon_session'] = check_coupons.coupon_discount_amount
                    request.session['coupon_id'] = check_coupons.id
                    messages.success(request, 'This coupon added successfully!')
                else:
                    coupon = False
                    messages.error(request, ' purchase minimum price!')
            else:
                messages.error(request, 'This coupon not valid!')

            address = Address.objects.filter(user=request.user)
            cart_count = Cart.objects.filter(user =request.user).count()
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            coupon_checkout = Coupon.objects.filter(is_available=True)
            if offer_price_total == 0:
                offer_price_total = False
            else:
                offer_price_total



            context = {
                'all_offer':all_offer,
                'offer' :offer_price_total,
                'coupon_checkout':coupon_checkout,
                'cartitems': cartitems,
                'total-price': total_price,
                'grand_total': grand_total,
                'address' : address,
                'cart_count':cart_count,
                'coupon' :cart_count,
                'wishlist_count':wishlist_count,
            }
            
           
        except:
            messages.error(request, 'This coupon not valid!')
            return redirect('checkout')
    # if total_price == 0 :
    #      redirect ('home')
    # else:
    #     return render(request,'checkout/checkout.html',context)
            
        
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    grand_total = 0
    offer_price = 0
    tax = 0
    offer_price_total= 0
    all_offer = 0
    for item in cartitems:
        if item.variant.product.offer:
            product_price = item.variant.product.product_price
            total_price += product_price * item.product_qty
            offer_price = item.variant.product.offer.discount_amount
            offer_price_total = offer_price * item.product_qty
            total_price = total_price - offer_price_total
            all_offer = all_offer + offer_price_total
            tax = total_price * 0.18
            
        else:
            product_price = item.variant.product.product_price
            total_price += product_price * item.product_qty
            tax = total_price * 0.18

    grand_total=total_price + tax

    address = Address.objects.filter(user= request.user)
    cart_count =Cart.objects.filter(user =request.user).count()
    wishlist_count =Wishlist.objects.filter(user=request.user).count()
    coupon_checkout =Coupon.objects.filter(is_available=True)
    coupon = False
    if offer_price_total ==0:
        offer_price_total =False
    else:
        offer_price_total

    context = {
        'all_offer':all_offer,
        'offer' :offer_price_total,
        'coupon_checkout':coupon_checkout,
        'cartitems': cartitems,
        'total_price': total_price,
        'grand_total': grand_total,
        'address': address,
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,  
        'coupon':coupon
    }
    if total_price==0:
       return redirect('home')
    else:
           
        return render(request,'checkout/checkout.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def placeorder(request):

    if request.method == 'POST':
        user=request.user
        coupon = request.POST.get('couponOrder')
        address_id=request.POST.get('address')
        if address_id is None:
            messages.error(request,'Address Field Is Mandatory!')
            return redirect('checkout')
        
        address=Address.objects.get(id=address_id)

        neworder =Order()
        neworder.user=user
        neworder.address = address
        neworder.payment_mode =request.POST.get('payment_method')
        neworder.message = request.POST.get('order_note')
        session_coupon_id=request.session.get('coupon_id')

        if session_coupon_id!=None:
            session_coupons =Coupon.objects.get(id=session_coupon_id)
        else:
            session_coupons = None
               
        neworder.coupon = session_coupons
        cart_items =Cart.objects.filter(user=request.user)
        cart_total_price = 0
        offer_total_price = 0
        tax = 0
        for item in cart_items:
            if item.variant.product.offer:
                product_price = item.variant.product.product_price
                cart_total_price += product_price * item.product_qty 
                offer_total_price =item.variant.product.offer.discount_amount
                offer_total_price = offer_total_price*item.product_qty
                cart_total_price = cart_total_price - offer_total_price
            else:
                product_price = item.variant.product.product_price
                cart_total_price += product_price * item.product_qty
        
        session_coupon=request.session.get('coupon_session')
        cart_total_price = cart_total_price - session_coupon
        neworder.total_price = cart_total_price
    
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)

        neworder.save()

        for item in cart_items:
            OrderItem.objects.create(
                order=neworder,
                variant=item.variant,
                price=item.variant.product.product_price,
                quantity=item.product_qty
            )

            product=Variant.objects.filter(id=item.variant.id).first()
            product.quantity -= item.product_qty
            product.save()
            # Delete the cart items after the order is placed 
            cart_items.delete()

        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'cod' or payment_mode == 'razorpay' :
            del request.session['coupon_session']
            del request.session['coupon_id']

            return JsonResponse({'status': "Your order has been placed successfully"})
           
    return redirect('checkout')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def addcheckoutaddr(request):
    if request.method == 'POST':
        address = Address()
        address.user = request.user
        address.first_name = request.POST.get('firstname')
        address.last_name = request.POST.get('lastname')
        address.country = request.POST.get('country')
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.pincode = request.POST.get('pincode')
        address.phone = request.POST.get('phone')
        address.email = request.POST.get('email')
        address.state = request.POST.get('state')
        address.order_note = request.POST.get('ordernote')
        address.payment_mode = request.POST.get('payment_method')
        address.save()
        messages.success(request,'Address Created Successfully!')

        return redirect('checkout')
    return redirect('checkout')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def deleteaddresscheckout(request,delete_id):
    address = Address.objects.filter(id=delete_id)
    address.delete()
    return redirect('placeorder')


def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def razarpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    tax =0

    for item in cart:
        if item.variant.product.offer:
            total_price = total_price + item.variant.product.product_price * item.product_qty
            total_offer = item.variant.product.offer.discount_amount*item.product_qty
            total_price = total_price-total_offer
            tax = total_price * 0.18
        else:
            total_price = total_price + item.variant.product.product_price * item.product_qty
            tax = total_price * 0.18
        session_coupon=request.session.get('coupon_session')
        print(session_coupon,'ooooooooooooorpppppppppprrrrrrrr')
        total_price = total_price - session_coupon 
        total_price += tax


    return JsonResponse({'total_price':total_price})























    


        




