# Generated by Django 4.2.3 on 2023-07-19 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('product_price', models.IntegerField()),
                ('product_image', models.ImageField(default='No image available', upload_to='photos/product')),
                ('product_quantity', models.IntegerField()),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
            ],
        ),
    ]
