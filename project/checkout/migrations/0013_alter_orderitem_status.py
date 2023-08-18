# Generated by Django 4.2.1 on 2023-08-17 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0012_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Return', 'Return'), ('pending', 'pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Shipped', 'Shipped')], default='pending', max_length=150),
        ),
    ]
