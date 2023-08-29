from django.shortcuts import render,redirect
from .models import Offer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
# Create your views here.


@login_required(login_url='admin_login1')
def offer (request):
    context={
        'offer' : Offer.objects.filter(is_available=True).order_by('id')
    }
    return render(request,'adminside/offer.html',context)

@login_required(login_url='admin_login1')
def add_offer(request):
    if request.method == 'POST':
        offername = request.POST.get('offername')
        discount = request.POST.get('discount')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if offername is None or offername.strip() == '':
            messages.error(request,'Cannot Blank Offer Name !')
            return redirect('offer')
        
        
        if discount.strip()== '':
            messages.error(request,'Cannot Blank Discount !')
            return redirect('offer')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('offer')
        
        if start_date >= end_date:
            messages.error(request,'Start date must be before end date! ')
            messages.error('offer')

        if start_date < timezone.now().date():
            messages.error(request,'start date cannot be past !')
            return redirect ('offer')
        offer = Offer.objects.create(
            offer_name=offername,
            discount_amount=discount,
            start_date=start_date,
            end_date= end_date
            
        )
        offer.save()
        messages.success(request,'Offer Added Successfully!')
        return redirect('offer')

@login_required(login_url='admin_login1')   
def edit_offer(request,offer_id):
    if request.method == 'POST':
        offername = request.POST.get('offername')
        discount = request.POST.get('discount')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if offername is None or offername.strip() == '':
            messages.error(request, "Order name cannot be blank.")
            return redirect('offer')
        
        if discount.strip() == '':
            messages.error(request, "Cannot blank Offer field")
            return redirect('offer')
        
        discount = int(discount)
        if discount <= 0:
            messages.error(request,'positive numbers only!')
            return redirect('offer')
        
        
        
        if Offer.objects.filter(offer_name=offername,is_available=True).exclude(id=offer_id).exists():
            messages.error(request,'Offer name already  exist!')
            return redirect ('offer')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('offer')
        if start_date >= end_date:
            messages.error(request, "Start date must be before end date.")
            return redirect('offer')
        if start_date < timezone.now().date():
            messages.error(request, "Start date cannot be in the past.")
            return redirect('offer')
        
        off = Offer.objects.get(id=offer_id)
        off.offer_name = offername
        off.discount_amount = discount
        off.start_date = start_date
        off.end_date = end_date
        off.save()
        messages.success(request,'Offer edited Successfully!.')
        return redirect('offer')
    offers = Offer.objects.get(id=offer_id)
    context={
        'offer' : offers
    }
    return render(request,'adminside/offer.html',context)

@login_required(login_url='admin_login1')
def delete_offer(request,delete_id):
    try:
        offer = Offer.objects.get(id=delete_id)
        offer.is_available = False
        offer.save()
        messages.success(request,'Offer Delete Successfully!')

    except offer.DoesNotExist:
        messages.error(request,'The specified offer doesnot exixt!.')
    return redirect('offer')


def offer_search(request):
    search = request.POST.get('search')
    if search is None or search.strip()=='':
        messages.error(request,'field cannot empty!.')
        return redirect('offer')
    offer = Offer.objects.filter(Q(offer_name__icontains=search) 
                                 | Q(discount_amount__icontains=search)
                                 | Q(start_date__icontains=search) 
                                 | Q(end_date__icontains=search)
                                 ,is_available =True)
    context={'offer':offer}

    if offer:
        pass
        return render (request,'adminside/offer.html',context)
    else:
        offer : False
        messages.error(request,'search not found!')
        return redirect('offer')
        


        


