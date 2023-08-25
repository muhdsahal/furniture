from django.contrib import admin
from .models import Order,Orderreturn,Order_cancelled
# Register your models here.

admin.site.register(Order)
admin.site.register(Orderreturn)
admin.site.register(Order_cancelled)