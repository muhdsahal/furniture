from django.shortcuts import render,redirect
from .models import Coupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

# Create your views here.
@login_required(login_url='admin_login1')
def coupon(request):
    context={
        'coupon' : Coupon.objects.filter(is_available= True).order_by('id')

    }
    return render(request,'adminside/coupon.html',context)


def add_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        min_price = request.POST.get('minimum_price')
        coupon_discount_amount = request.POST.get('coupon_discount_amount')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if coupon_name is None or coupon_name.strip()=='':
            messages.error(request,'Cannnot Blank Name!')
            return redirect ('coupon')
        if not re.search(r'\b[A-Z0-9a-z]{2,}\b', coupon_code):
            messages.error(request,'Coupen code must inlcude letters and numbers!')
            return redirect('coupon')
        if min_price.strip() == '':
            messages.error(request,'Cannot blank minimum price !')
            return redirect('coupon')
        
        min_price = int(min_price)
        if not min_price >=0:
            messages.error(request,'Minimum price must be want to positive numbers!')
            return redirect('coupon')

        if coupon_discount_amount .strip() == '':
            messages.error(request,'Cannot blank coupon_discount_amount')
            return redirect('coupon')
        
        coupon_discount_amount = int(coupon_discount_amount)
        if not coupon_discount_amount >= 0:
            messages.error(request,'Discount must be want to positive numbers!')
            return redirect('coupon')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('coupon')
        
        if start_date >= end_date:
            messages.error(request,'Start date must be before end date!.')
            return redirect('coupon')
        
        if start_date < timezone.now().date():
            messages.error(request, "Start date cannot be in the past.")
            return redirect('coupon')
        
        coupon =Coupon.objects.create(
            coupon_name = coupon_name,
            coupon_code =coupon_code,
            min_price = min_price,
            coupon_discount_amount=coupon_discount_amount,
            start_date =start_date,
            end_date =end_date, 

        )
        coupon.save()
        messages.success(request,'Coupon Added Successfully!')
        return redirect('coupon')

@login_required(login_url='admin_login1')    
def edit_coupon(request, coupon_id):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        min_price = request.POST.get('minimum_price')
        coupon_discount_amount = request.POST.get('coupon_discount_amount')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        if coupon_name is None or coupon_name.strip() == '':
            messages.error(request, "Cannot blank coupon name!")
            return redirect('coupon')
        if not re.search(r'\b[A-Z0-9a-z]{2,}\b', coupon_code):
            messages.error(request, " Coupen code must inlcude letters and numbers!")
            return redirect('coupon')
        if min_price.strip() == '':
            messages.error(request, "Cannot blank minimum price!")
            return redirect('coupon')    
        min_price=int( min_price)
        if not min_price >=0 :
            messages.error(request, "minimum price must be want to positive numbers!")
            return redirect('coupon')
        if coupon_discount_amount.strip() == '':
            messages.error(request, "Cannot blank Discount!")
            return redirect('coupon')
        coupon_discount_amount =int(coupon_discount_amount)
        if not coupon_discount_amount >=0 :
            messages.error(request, "Discount must be want to positive numbers!")
            return redirect('coupon')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('coupon')
        if start_date >= end_date:
            messages.error(request, "Start date must be before end date.")
            return redirect('coupon')
        if start_date < timezone.now().date():
            messages.error(request, "Start date cannot be in the past.")
            return redirect('coupon')
        if Coupon.objects.filter(coupon_name=coupon_name ,is_available=True).exclude(id=coupon_id).exists():
            messages.error(request, 'name already exists!')
            return redirect('coupon')
        
        
        coupon_edit = Coupon.objects.get(id=coupon_id)
        coupon_edit.coupon_edite_name = coupon_name
        coupon_edit.coupon_code = coupon_code
        coupon_edit.min_price = min_price
        coupon_edit.coupon_discount_amount = coupon_discount_amount
        coupon_edit.start_date = start_date
        coupon_edit.end_date = end_date
        coupon_edit.save()
        messages.success(request, "Coupon edited edited successfully!")
        return redirect('coupon')
    coupon: Coupon.objects.get(id=coupon_id)
    context ={ 
     'coupon':coupon,
    }
    return render(request, 'adminside/coupon.html', context)

@login_required(login_url='admin_login1')
def delete_coupon(request, coupon_id):
    try:
        coupon_delete = Coupon.objects.get(id=coupon_id)  
        coupon_delete.is_available = False
        coupon_delete.save()
        messages.success(request, "coupon deleted successfully!")
        return redirect('coupon')
    except:
        messages.error(request, "The specified coupon does not exist!")
    return redirect('coupon')

@login_required(login_url='admin_login1')
def coupon_search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        if search is None or search.strip() == '':
            messages.error(request, 'Field cannot be empty!')
            return redirect('coupon')

        try:
            coupon_discount_amount = float(search)
            coupons = Coupon.objects.filter(
                Q(coupon_name__icontains=search)
                | Q(coupon_code__icontains=search)
                | Q(min_price__icontains=search)
                | Q(coupon_discount_amount=coupon_discount_amount),
                is_available=True
            )
        except ValueError:
            messages.error(request, 'Invalid search input for coupon_discount_amount')
            return redirect('coupon')
        
        if coupons:
            # Pass the 'coupons' queryset to the template
            context = {'coupon': coupons}
            return render(request, 'adminside/coupon.html', context)
        else:
            messages.error(request, 'Search Not Found!')
            return redirect('coupon')
    else:
        return redirect('coupon')  # Redirect if the request method is not POST




        

            





    