# Generated by Django 4.2.3 on 2023-07-19 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.CharField(max_length=200, unique=True)),
                ('categories_image', models.ImageField(default='no image avilable', upload_to='#')),
                ('categories_description', models.SlugField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
    ]
