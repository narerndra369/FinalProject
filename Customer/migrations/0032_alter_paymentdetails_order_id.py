# Generated by Django 3.2 on 2025-03-14 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0031_alter_paymentdetails_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.useroder'),
        ),
    ]
