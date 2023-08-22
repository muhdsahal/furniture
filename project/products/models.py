from django.db import models
from django.utils.text import slugify
from categories.models import Category
from offer.models import Offer
# Create your models here.


class Color(models.Model):
    color_name = models.CharField(max_length=50)
    color_code =models.CharField(max_length=15)
    is_available=models.BooleanField(default=True)

    def __str__(self) :
        return self.color_name

class Product(models.Model):
    product_name = models.CharField(unique=True, max_length=50,null=True, blank=True)
    product_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True, blank=True)
    product_description = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True )
    is_available=models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name 
