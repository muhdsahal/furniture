# Generated by Django 4.2.3 on 2023-08-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Return', 'Return'), ('pending', 'pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing')], default='pending', max_length=150),
        ),
    ]