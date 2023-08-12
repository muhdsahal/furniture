# Generated by Django 4.2.1 on 2023-08-12 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled'), ('pending', 'pending'), ('Return', 'Return')], default='pending', max_length=150),
        ),
    ]