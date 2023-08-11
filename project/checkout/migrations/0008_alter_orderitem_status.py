# Generated by Django 4.2.3 on 2023-08-11 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Return', 'Return'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Delivered', 'Delivered'), ('pending', 'pending')], default='pending', max_length=150),
        ),
    ]
