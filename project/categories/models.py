from django.shortcuts import render
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your views here.
class Category(models.Model):
    categories = models.CharField(max_length=100)
    categories_description = models.TextField(max_length=300)  # This is an example of a TextField for the description
    # categories_image = models.ImageField(upload_to='categories_images/',default='No Image available')
    slug = models.SlugField(max_length=250,unique=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.categories)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        app_label = 'categories'
        verbose_name_plural='categories'


    def get_url(self):
        return reverse('product_by_Category', args={self.slug} )

    def __str__(self):
        return self.categories  

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/variant',default='No Image Avilable')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Image for {self.category.categories}"
