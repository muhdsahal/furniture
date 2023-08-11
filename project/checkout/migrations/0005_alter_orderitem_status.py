# Generated by Django 4.2.3 on 2023-08-11 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('Processing', 'Processing'), ('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='pending', max_length=150),
        ),
    ]
