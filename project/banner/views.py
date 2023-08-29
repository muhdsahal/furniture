from django.shortcuts import render,redirect

from categories.models import Category
from .models import banner
from django.contrib import messages
# Create your views here.


def banners(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    banners_display = banner.objects.all().order_by('id')
    category_display =Category.objects.filter(is_available=True)
    return render(request, 'banner/banner.html',{'banner' :banners_display,'categorys':category_display})

def add_banners(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST.get('banner_name')
        image = request.FILES.get('banner_image', None)
       
        description = request.POST['banner_discription']

        # Validation
        if name.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('banners')

        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('banners')
        
        if banner.objects.filter(banner=name).exists():
            messages.error(request, 'banner name already exists')
            return redirect('banners')

        ban = banner(
            banner=name,
            banner_image=image,
       
            caption=description,
        )
        ban.save()
        messages.success(request, 'banner added successfully! ')
        return redirect('banners')

    return render(request, 'banner/banner.html')

def edit_banner(request, edit_banner_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        name = request.POST['banner_name']
     
        description = request.POST['banner_discription']
# validation
        if name.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('banners')
        if banner.objects.filter(banner=name).exists():
            check = banner.objects.get(id = edit_banner_id)
            if name == check.banner:
                pass
            else:
                messages.error(request, 'Banner name already exists')
                return redirect('banners')

        try:
            cat = banner.objects.get(id=edit_banner_id)
            eimage = request.FILES['banner_image']
            cat.banner_image = eimage
            cat.save()
        except:
            pass 

        cat = banner.objects.get(id=edit_banner_id)
        cat.banner = name
      
        cat.caption = description
        cat.save()
        messages.success(request, 'banner edited successfully! ')
        return redirect('banners')
    banners = banner.objects.filter(id=edit_banner_id)       
    return render(request, 'banner/banner.html', {'banners': banners})

# Delete 
def delete_banner(request,delete_banner_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    banners = banner.objects.get(id=delete_banner_id)
    banners.is_available =False
    banners.save()
    messages.success(request, 'banner deleted successfully! ')
    
    return redirect('banners')