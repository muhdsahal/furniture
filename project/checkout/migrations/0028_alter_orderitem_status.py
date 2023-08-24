# Generated by Django 4.2.3 on 2023-08-24 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0027_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('pending', 'pending')], default='pending', max_length=150),
        ),
    ]