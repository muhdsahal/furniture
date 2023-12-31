# Generated by Django 4.2.1 on 2023-08-12 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('pending', 'pending'), ('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Processing', 'Processing')], default='pending', max_length=150),
        ),
    ]
