# Generated by Django 4.2.3 on 2023-08-17 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_remove_product_product_image1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_quantity',
        ),
    ]
