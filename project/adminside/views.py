from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import Banner
from categories.models import Category
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout

# verification email
from user.models import UserOTP
from user.views import validateemail,validatepassword
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re

# # Create your views here.
def admin_signup(request):

    if request.method == 'POST':

        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            user=User.objects.get(email=get_email)

            if int(get_otp)==UserOTP.objects.filter(user=user).last().otp:
                user.is_active=True
                user.save()
                auth.login(request,user)
                UserOTP.objects.filter(user=user).delete()
                return redirect('dashboard')
            else:
                messages.warning(request,f'you entered wrong otp')
                return render(request,'adminside/admin_signup.html',{'otp':True,'user':user})
        else:
            username=request.POST['username']
            email=request.POST['email']
            password1=request.POST['password1']

            context={
                'pre_username':username,
                'pre_email':email,
                'pre_password':password1,
            }


            if username.strip()=='' or password1.strip()=='' or email.strip()=='':
                messages.error(request,'field cannot empty !')
                return render(request,'adminside/admin_signup.html',context)
            
            elif  User.objects.filter(username=username):
                messages.error(request,'username already exist !')
                context['pre_username']=''
                return render(request,'adminside/admin_signup.html',context)
            
            elif not re.match(r'^[a-zA-Z\s]*$',username):
                messages.error(request,'username  should only alphabets !')
                context['pre_username']=''
                return render(request,'adminside/admin_signup.html',context)
            
            elif User.objects.filter(email=email):
                messages.error(request,'email is already exist !')
                context['pre_email']=''
                return render(request,'adminside/admin_signup.html',context)
            
            email_check=validateemail(email)
            if email_check is False:
                messages.error(request,'email not valid')
                context['pre_email']=''
                return render(request,'adminside/admin_signup.html',context)

            password_check=validatepassword(password1)
            if password_check is False:
                messages.error(request,'password is invalid !')
                context['pre_password']=''
                return render(request,'adminside/admin_signup.html',context)
            
            user=User.objects.create_user(username=username,email=email,password=password1)
            user.is_active=False
            user.is_superuser=True
            user.save()
            user_otp=random.randint(100000,999999)
            UserOTP.objects.create(user=user,otp=user_otp)
            mess=f' Hello \t {user,username}, \n your OTP to varifie your account for Aranoz is {user_otp} \n  Thank You !'
            send_mail(
                'Welcome tp Aranoz varifie your OTP',
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
                )
            return render(request,'adminside/admin_signup.html',{'otp':True,'user':user})

    return render (request,'adminside/admin_signup.html')

def admin_login1(request):


    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']


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
                messages.warning(request,'your account has been bloked')
                return redirect('admin_login1')
        else:
            messages.error(request,'invalid username or password')
            return redirect('admin_login1')
    return render(request,'adminside/admin_login1.html')

def dashboard(request):
    return render(request,'adminside/dashboard.html')



@login_required(login_url='admin_login1')
def admin_logout1(request):
    logout(request)
    return redirect('admin_login1')

@login_required(login_url=admin_login1)
def usermanagment_1(request):
    users=User.objects.all().order_by('id')
    return render(request,'adminside/usermanagement.html',{'users':users})


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

def banner(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    dict_banner = {
        'banner':Banner.objects.all(),
        'category':Category.objects.all()
    }
    return render(request,'banner/banner.html',dict_banner)
def createbanner(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name=request.POST.get('banner_name')
        discription=request.POST.get('banner_discription')
        categories=request.POST.get('categories')
        image=request.FILES.get('image',None)

        if name.strip() == '':
            messages.error(request,'name is empty !')
            return render('banner')
        if not image:
            messages.error(request,'image not uploaded !')
            return render('banner')
        
        cat=Category.objects.filter(id=categories)
        ban=Banner(
        banner_image=image,
        banner_name=name,
        banner_discription=discription,
        Category=cat,
        )
        ban.save()
    return redirect('banner')








