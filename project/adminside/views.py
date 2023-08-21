from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import Banner
from categories.models import Category
from order.models import Order
from checkout.models import OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from datetime import date, datetime,timedelta
from itertools import groupby
import csv
import io
from django.db.models.functions import TruncMonth
from django.http import FileResponse
from django.views import View
from fpdf import FPDF
from django.db.models import Prefetch
# verification email
from user.models import UserOTP
from user.views import validateemail,validatepassword
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re

#adminde
# def admin_signup(request):

#     if request.method == 'POST':

#         get_otp=request.POST.get('otp')
#         if get_otp:
#             get_email=request.POST.get('email')
#             user=User.objects.get(email=get_email)

#             if int(get_otp)==UserOTP.objects.filter(user=user).last().otp:
#                 user.is_active=True
#                 user.save()
#                 auth.login(request,user)
#                 UserOTP.objects.filter(user=user).delete()
#                 return redirect('dashboard')
#             else:
#                 messages.warning(request,f'you entered wrong otp')
#                 return render(request,'adminside/admin_signup.html',{'otp':True,'user':user})
#         else:
#             username=request.POST.get('username')
#             email=request.POST.get('email')
#             password1=request.POST('password1')

#             context={
#                 'pre_username':username,
#                 'pre_email':email,
#                 'pre_password':password1,
#             }


#             if username.strip()=='' or password1.strip()=='' or email.strip()=='':
#                 messages.error(request,'field cannot empty !')
#                 return render(request,'adminside/admin_signup.html',context)
            
#             elif  User.objects.filter(username=username):
#                 messages.error(request,'username already exist !')
#                 context['pre_username']=''
#                 return render(request,'adminside/admin_signup.html',context)
            
#             elif not re.match(r'^[a-zA-Z\s]*$',username):
#                 messages.error(request,'username  should only alphabets !')
#                 context['pre_username']=''
#                 return render(request,'adminside/admin_signup.html',context)
            
#             elif User.objects.filter(email=email):
#                 messages.error(request,'email is already exist !')
#                 context['pre_email']=''
#                 return render(request,'adminside/admin_signup.html',context)
            
#             email_check=validateemail(email)
#             if email_check is False:
#                 messages.error(request,'email not valid')
#                 context['pre_email']=''
#                 return render(request,'adminside/admin_signup.html',context)

#             password_check=validatepassword(password1)
#             if password_check is False:
#                 messages.error(request,'password is invalid !')
#                 context['pre_password']=''
#                 return render(request,'adminside/admin_signup.html',context)
            
#             user=User.objects.create_user(username=username,email=email,password=password1)
#             user.is_active=False
#             user.is_superuser=True
#             user.save()
#             user_otp=random.randint(100000,999999)
#             UserOTP.objects.create(user=user,otp=user_otp)
#             mess=f' Hello \t {user.username}, \n your OTP to varifie your account for Aranoz is {user_otp} \n  Thank You !'
#             send_mail(
#                 'Welcome tp Aranoz varifie your OTP',
#                 mess,
#                 settings.EMAIL_HOST_USER,
#                 [user.email],
#                 fail_silently=False
#                 )
#             return render(request,'adminside/admin_signup.html',{'otp':True,'user':user})

#     return render (request,'adminside/admin_signup.html')

#adminlogin
def admin_login1(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')


        if username.strip() =='' or password.strip()=='':
            messages.error(request,'feild cannot empty !')
            return redirect('admin_login1')
        
        user=authenticate(username=username,password=password)

        if user is not None:

            if user.is_active:
                if user.is_superuser:
                    login(request,user)
                    return  redirect('dashboard') #dashboard
                else:
                    messages.warning(request,'your not admin')
                return redirect('admin_login1')
            
            else:
                messages.warning(request,'your account has been blocked')
                return redirect('admin_login1')
        else:
            messages.error(request,'invalid username or password')
            return redirect('admin_login1')
    return render(request,'adminside/admin_login1.html')

def dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    return render(request,'adminside/dashboard.html')


#adminlogout
@login_required(login_url='admin_login1')
def admin_logout1(request):
    logout(request)
    return redirect('admin_login1')

#usermanagemant
@login_required(login_url='admin_login1')
def usermanagment_1(request):
    users=User.objects.all().order_by('id')
    return render(request,'adminside/usermanagement.html',{'users':users})

#block unblock
@login_required(login_url='admin_login1')
def blockuser(request,user_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    user= User.objects.get(id=user_id)
    if user.is_active:
        user.is_active=False
        user.save()
    else:
        user.is_active=True
        user.save()
    return redirect('usermanagement_1')

#banner area
# def banner(request):
#     if not request.user.is_superuser:
#         return redirect('admin_login1')
#     dict_banner = {
#         'banner':Banner.objects.all(),
#         # 'category':Category.objects.all()
#     }
#     return render(request,'banner/banner.html',dict_banner)

@login_required(login_url='admin_login1')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            # Filter orders based on the selected date range
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date >=  end_date:
                messages.error(request,'Start Date Must Be Before End Date!')
                return redirect('sales_report')
            if end_date > date.today():
                messages.error(request, "End date cannot be in the future.")
                return redirect('sales_report')
            orders = Order.objects.filter(created_at__date__range=(start_date,end_date))
            recent_orders = orders.order_by('-created_at')
        else:
            # If no date range is selected, fetch recent 10 orders
            recent_orders =Order.objects.order_by('-created_at')[:10]
            orders=Order.objects.all()

    # Calculate total sales and total orders        
    total_sales = sum(order.total_price for order in orders)
    total_orders =orders.count()

    # Calculate sales by status
    sales_by_status = {
        'Pending': orders.filter(order_status= 1).count(),
        'Processing': orders.filter(order_status=2).count(),
        'Shipped': orders.filter(order_status=3).count(),
        'Delivered': orders.filter(order_status=4).count(),
        'Cancelled': orders.filter(order_status=5).count(),
        'Return': orders.filter(order_status=6).count(),
    }

    sales_report = {
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'total_sales': total_sales,
        'total_orders': total_orders,
        'sales_by_status': sales_by_status,
        'recent_orders': recent_orders,
    }

    return render(request, 'adminside/salesreport.html', {'sales_report': sales_report})

@login_required(login_url='admin_login1')
def export_csv(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no', 'Orderd at', 'product_name', 'product_price', 'product_quantity'])

    orders = Order.objects.all()
    for order in orders:
        order_items = OrderItem.objects.filter(order=order).select_related('variant')  # Use select_related to optimize DB queries
        grouped_order_items = groupby(order_items, key=lambda x: x.order_id)
        for order_id, items_group in grouped_order_items:
            items_list = list(items_group)
            for order_item in items_list:
                writer.writerow([
                    order.user.first_name if order_item == items_list[0] else "",
                    order.total_price if order_item == items_list[0] else "",
                    order.payment_mode if order_item == items_list[0] else "",
                    order.tracking_no if order_item == items_list[0] else "",
                    order.created_at if order_item == items_list[0] else "",  # Only include date in the first row
                    order_item.variant.product.product_name,  # Replace 'product_name' with the actual attribute in your Product model
                    order_item.price,
                    order_item.quantity,
                ])

    return response

@login_required(login_url='admin_login1')
def generate_pdf(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.pdf'
    w_pt = 8.5 * 40  # 8.5 inches width
    h_pt = 11 * 20   # 11 inches height   

    pdf = FPDF(format=(w_pt, h_pt))
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)  # Enable auto page break with 15mm margin

    # Set font styles
    pdf.set_font('Arial', 'B', 12)  # Reduce font size for better readability

    # Header Information
    pdf.cell(0, 10, 'Order Details Report', 0, 1, 'C')
    pdf.cell(0, 10, str(datetime.now()), 0, 1, 'C')
    # Table Data
    data = [['User', 'Total Price', 'Payment Mode', 'Tracking No', 'Ordered At', 'Product Name', 'Product Price', 'Product Quantity']]
    orders = Order.objects.all().prefetch_related(
        Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('variant'))
    )
    for order in orders:
        order_items = order.orderitem_set.all()
        for index, order_item in enumerate(order_items):
            data.append([
                order.user.first_name if index == 0 else "",
                order.total_price if index == 0 else "",
                order.payment_mode if index == 0 else "",
                order.tracking_no if index == 0 else "",
                str(order.created_at.date()) if index == 0 else "",
                order_item.variant.product.product_name,
                order_item.price,
                order_item.quantity,
            ])
    # Create Table
    col_width = 40  
    row_height = 10
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln()
    response.write(pdf.output(dest='S').encode('latin1'))  
    return response















