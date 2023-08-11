# Generated by Django 4.2.3 on 2023-08-11 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Return', 'Return'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled')], default='pending', max_length=150),
        ),
    ]
