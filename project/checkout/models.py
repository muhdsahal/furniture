from django.db import models
from variant.models import Variant
from userprofile.models import Address
from products.models import Product
from django.contrib.auth.models  import User
from datetime import timedelta,timezone

# Create your models here.
class Orderstatus(models.Model):
    order_status =models.CharField(max_length=100)

    def __str__(self):
        return self.order_status
class Itemstatus(models.Model):
    item_status = models.CharField(max_length=100)

    def __str__(self):
        return self.item_status
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    total_price =models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id =models.CharField(max_length=250,null=True)
    message=models.TextField(null=True)
    tracking_no =models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True)
    order_status =models.ForeignKey(Orderstatus,on_delete=models.CASCADE ,null=True,default=1)
    return_total_price =models.IntegerField(null=True)

    @property
    def expected_delivery(self):
        return self.created_at + timedelta(days=4)

    def __str__(self):
        return f"{self.id,self.tracking_no}"
    

 
class OrderItem(models.Model):
        
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,null=True)
    price=models.FloatField(null=True)
    quantity=models.IntegerField(null=False)
    orderitem_status =models.ForeignKey(Itemstatus, on_delete=models.CASCADE ,null=True,default=1)
    orderstatuses = {
        ('pending','pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return', 'Return')
    }
    status=models.CharField(max_length=150,choices=orderstatuses,default='pending')

    def __str__(self):
        return f"{self.order.id,self.order.tracking_no}"


    

    