# Generated by Django 4.2.1 on 2023-07-27 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0005_remove_banner_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Banner',
        ),
    ]