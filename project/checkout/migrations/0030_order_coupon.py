# Generated by Django 4.2.3 on 2023-08-30 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
        ('checkout', '0029_alter_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coupon.coupon'),
        ),
    ]