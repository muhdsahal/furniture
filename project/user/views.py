from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.csrf import csrf_protect
# email verification
from user.models import UserOTP


import re
from django.core.validators import validate_email
import random
from django.core.mail import send_mail
from django.conf import settings

@csrf_protect
def user_signup(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            user = User.objects.get(email=get_email)

            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                auth.login(request, user)
                UserOTP.objects.filter(user=user).delete()
                return redirect('home')
            else:
                messages.warning(request, 'You entered a wrong OTP')
                return render(request, 'user\signup.html', {'otp': True, 'user': user})
        else:
            firstname = request.POST['fname']
            lastname = request.POST['lname']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            context = {
                'pre_firstname': firstname,
                'pre_lastname': lastname,
                'pre_username': username,
                'pre_email': email,
                'pre_password1': password1,
                'pre_password2': password2
            }

            if username.strip() == '' or password1.strip() == '' or password2.strip() == '' or email.strip() == '' or firstname.strip() == '' or lastname.strip() == '':
                messages.error(request, 'Fields cannot be empty!')
                return render(request, 'user\signup.html', context)

            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                context['pre_username'] = ''
                return render(request, 'user\signup.html', context)

            elif not re.match(r'^[a-zA-Z\s]*$', username):
                messages.error(request, 'Username should only contain alphabets!')
                context['pre_username'] = ''
                return render(request, 'user\signup.html', context)

            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                context['pre_email'] = ''
                return render(request, 'user\signup.html', context)

            elif password1 != password2:
                messages.error(request, 'Passwords do not match!')
                context['pre_password1'] = ''
                context['pre_password2'] = ''
                return render(request, 'user\signup.html', context)

            email_check = validate_email(email)
            if email_check is False:
                messages.error(request, 'Invalid email!')
                context['pre_email'] = ''
                return render(request, 'user\signup.html', context)

            password_check = validate_password(password1)
            if password_check is False:
                messages.error(request, 'Please enter a strong password!')
                context['pre_password1'] = ''
                context['pre_password2'] = ''
                return render(request, 'user\signup.html', context)

            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password1)
            user.is_active = False
            user.save()
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            message = f'Hello {user.username},\nYour OTP to verify your account for Aranoz  is {user_otp}\nThank you.'
            send_mail(
                "Welcome to Aranoz - Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return render(request, 'user\signup.html', {'otp': True, 'user': user})
    return render(request, 'user\signup.html')


def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validatepassword(password1):
    try:
        validate_password(password1)
        return True
    except ValidationError:
        return False


def user_login1(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        if username == '' or password == '':
            messages.error(request, "Fields cannot be empty!")
            return redirect('user_login1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Your account has been blocked!')
                return redirect('user_login1')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('user_login1')

    return render(request, 'user/login.html')


@login_required(login_url='user_login1')
def logout1(request):
    logout(request)
    return redirect('home') 


def forgot_password(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                user=User.objects.get(email = get_email)
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                Pass = validatepassword(password1)
                if password1 == password2:
                    if Pass is False:
                        context = {
                            'pre_otp': get_otp,
                            }
                        messages.info(request,"enter strong password")
                        return render (request,'user/password_forgot.html',context)
                    user.set_password(password1)
                    user.save()
                    UserOTP.objects.filter(user=usr).delete()
                    return redirect ('user_login1')
                else:
                    messages.error(request,'password dosent match')
            else:
                messages.warning(request,f" you entered  a wrong otp")
                return render(request,'user/password_forgot.html',{'otp':True,'usr':usr})
            #user registration checking
        else:
            email=request.POST['email']

            check=[email]
            for values in check:
                if values == '':
                    context= {
                        'pre_email':email
                    }
                    return render(request,'user/password_forgot.html',context)
                else:
                    pass

            result=validateemail(email)
            if result is False:
                context ={
                    'pre_email':email
                }
                messages.error(request,'enter valid email')
                return render(request,'user/password_forgot.html',context)
            else:
                pass
            if User.objects.filter(email=email).exists():
                usr = User.objects.get(email=email)
                user_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user=usr, otp=user_otp)
                message = f'Hello\t{usr.username},\n Your OTP to verify your account for Aranoz is {user_otp}\n Thanks' 
                send_mail(
                        "Welcome to Aranoz Verify Email",
                        message,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                return render (request, 'user/password_forgot.html', {'otp': True, 'usr': usr}) 
            else:
                messages.info(request, 'you have not an account')
                return render(request, 'user/password_forgot.html')
    return render(request, 'user/password_forgot.html') 

























    #             if password1.strip() == '' or password2.strip() == '':
    #                 messages.error(request, 'Field cannot be empty!')
    #                 return render(request, 'user/password_forgot.html', {'otp': True, 'user': user, 'pre_otp': get_otp})
                
    #             elif password1 != password2:
    #                 messages.error(request, 'Passwords do not match!')
    #                 return render(request, 'user/password_forgot.html', {'otp': True, 'user': user, 'pre_otp': get_otp})
                    
    #             Pass = validatepassword(password1)
    #             if Pass is False:
    #                 messages.error(request, 'Please enter a strong password!')
    #                 return render(request, 'user/password_forgot.html', {'otp': True, 'user': user, 'pre_otp': get_otp})
    #             user.set_password(password1)
    #             user.save()
    #             UserOTP.objects.filter(user=user).delete()
    #             messages.success(request, 'Your password has been changed successfully!')
    #             return redirect('user_login1')
    #         else:
    #             messages.warning(request, 'You entered the wrong OTP!')
    #             return render(request, 'user/password_forgot.html', {'otp': True, 'user': user})  
    #     else:
    #         email = request.POST['email']
            
    #         if email.strip() == '':
    #             messages.error(request, 'Field cannot be empty!')
    #             return render(request, 'user/password_forgot.html')
            
    #         email_check = validateemail(email)
    #         if email_check is False:
    #             messages.error(request, 'Email not valid!')
    #             return render(request, 'user/password_forgot.html')
        
    #         if User.objects.filter(email=email):
    #             user = User.objects.get(email=email)
    #             user_otp = random.randint(100000, 999999)
    #             UserOTP.objects.create(user=user, otp=user_otp)
    #             message = f'Hello\t{user.username},\n Your OTP to verify your account for Aranoz is {user_otp}\n Thanks' 
    #             send_mail(
    #                 "Welcome to Aranoz Verify Email",
    #                 message,
    #                 settings.EMAIL_HOST_USER,
    #                 [user.email],
    #                 fail_silently=False
    #             )
    #             return render (request, 'user/password_forgot.html', {'otp': True, 'user': user}) 
    #         else:
    #             messages.error(request, 'Email does not exist!')
    #             return render(request, 'user/password_forgot.html')
    # return render(request, 'user/password_forgot.html') 




 # try:
            #     user = User.objects.get(email=get_email)
            # except User.DoesNotExist:
            #     messages.warning(request, 'User with this email does not exist!')
            #     return render(request, 'user/password_forgot.html')