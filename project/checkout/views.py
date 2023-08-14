from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.models import Cart
from userprofile.models import Address
from django.contrib.auth.models import User
from django.contrib import messages
from products.models import *
from checkout.models import Order, OrderItem
from django.shortcuts import render, redirect
from variant.models import Variant,VariantImage
import random
import string
import re
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def checkout(request):
    cartitems= Cart.objects.filter(user=request.user)
    total_price = 0
    grand_total = 0
    tax = 0
    for item in cartitems:
        total_price = total_price+item.product.product_price * item.product_qty
        tax = total_price * 0.18
        grand_total=total_price + tax
    address = Address.objects.filter(user=request.user)
    context = {
        'cartitems': cartitems,
        'total-price': total_price,
        'grand_total': grand_total,
        'address' : address,
    }
    return render(request,'checkout/checkout.html',context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login1')
def placeorder(request):

    if request.method == 'POST':
        neworder =Order()
        neworder.user=request.user
        address_id=request.POST.get('address')

        if address_id is None:
            messages.error(request,'Address Field Is Mandatory!')
            return redirect('checkout')
        
        address=Address.objects.filter(id=address_id)
        neworder.address = address
        payment_method =request.POST.get('payment_method')

        if payment_method is None:
            messages.error(request,'Please Select Any Payment Option ! ')
            return redirect('checkout')
        
        neworder.payment_mode = payment_method
        neworder.payment_id = request.POST.get('payment_id')
        cart =Cart.objects.filter(user=request.user)
        cart_total_price = 0
        tax = 0
        for item in cart:
            cart_total_price +=item.product.product_price * item.product_qty
            tax=cart_total_price * 0.18
            cart_total_price + tax

        neworder.total_price =cart_total_price
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)

        neworder.save()

        neworderitems =Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.Create(
                order=neworder,
                variant=item.variant,
                price=item.variant.product.product_price,
                quantity=item.product_qty
            )

            prod=Variant.objects.filter(id=item.variant.id).first()
            prod.quantity -= item.product_qty
            prod.save()

        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'cod':
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse({'status':'Your Order Has Been Placed Success Fully'})
        
        Cart.objects.filter(user=request.user).delete()
    return redirect('checkout')


def generate_random_payment_id(length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))


def razarpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    total_offer =0
    for item in cart:
        total_price = total_price + item.variant.product.product_price * item.product_qty
    total_price = total_price- total_offer

    return JsonResponse({'total_price':total_price})























    


        




