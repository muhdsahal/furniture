from django.db import models
from django.contrib.auth.models import User

class Userdp(models.Model):
    profilephoto=models.ImageField(upload_to='photos/variant',default='No Image Avilable')
    


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name =models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    order_note=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.id}"

class Wallet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    wallet=models.PositiveIntegerField(null=True)