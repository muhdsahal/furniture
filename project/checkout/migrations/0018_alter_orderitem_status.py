# Generated by Django 4.2.3 on 2023-08-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0017_remove_orderitem_product_orderitem_variant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('pending', 'pending'), ('Return', 'Return'), ('Delivered', 'Delivered')], default='pending', max_length=150),
        ),
    ]
