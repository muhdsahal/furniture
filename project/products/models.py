from django.db import models
from django.utils.text import slugify
from categories.models import Category
# Create your models here.


class Product(models.Model):
    product_name = models.CharField(unique=True, max_length=50,null=True, blank=True)
    product_price = models.IntegerField(null=True, blank=True)
    product_image = models.ImageField(upload_to='photos/product', default='No image available')
    product_quantity=models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    is_availble=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name 
