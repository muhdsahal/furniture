from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class category(models.Model):
    categories=models.CharField(max_length=200,unique=True)
    categories_image=models.ImageField(upload_to='#',default='no image avilable')
    categories_description=models.SlugField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug= slugify(self.categories)
        super(category,self).save(*args,**kwargs)

        class Meta:
            verbose_name='category'
            verbose_name_plural='categories'

        def get_url(self):
            return reverse('product_by_category',args={self.slug})
        
        def __str__(self):
            return self.categories