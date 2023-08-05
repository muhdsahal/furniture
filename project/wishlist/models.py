from django.db import models
from products.models import Product
from django.contrib.auth.models import User


# Create your models here.
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)