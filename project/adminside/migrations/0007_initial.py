# Generated by Django 4.2.1 on 2023-07-27 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0004_initial'),
        ('adminside', '0006_delete_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_image', models.ImageField(upload_to='photos/banner')),
                ('banner_name', models.CharField(max_length=200)),
                ('banner_discription', models.CharField(max_length=200)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
            ],
        ),
    ]
