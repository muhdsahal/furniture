from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from variant.models import Variant
# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(User ,on_delete=models.CASCADE)
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}"