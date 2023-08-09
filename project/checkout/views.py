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
def placeholder(request):
    



