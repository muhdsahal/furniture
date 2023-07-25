from django.db import models
from categories.models import Category


class Banner(models.Model):
    banner_image=models.ImageField(upload_to='photos/banner')
    banner_name=models.CharField(max_length=200)
    banner_discription=models.CharField(max_length=200)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.banner_name