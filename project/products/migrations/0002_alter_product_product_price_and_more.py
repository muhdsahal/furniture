# Generated by Django 4.2.3 on 2023-07-20 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]