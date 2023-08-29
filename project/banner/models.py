from django.db import models

from categories.models import Category

# Create your models here.
class banner(models.Model):
    banner = models.CharField(max_length=200)
    banner_image = models.ImageField(upload_to='photos/brand',default='No image available')
    caption=models.TextField(max_length=200)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True )
    is_available = models.BooleanField(default=True)
  

    def __str__(self):
        return self.banner
