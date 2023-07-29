from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    user=models.foreignKey(User,on_delete=models.CASCADE)
    first_name =models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address=models.models.CharField(max_length=50)
    country=models.models.CharField(max_length=50)
    state=models.models.CharField(max_length=50)
    city=models.models.CharField(max_length=50)
    pincode=models.models.CharField(max_length=50)
    order_note=models.models.CharField(max_length=50)
    def __str__(self):
        return f"{self.id}"

