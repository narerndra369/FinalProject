# Generated by Django 3.2 on 2025-03-14 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0030_auto_20250314_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='order_id',
            field=models.IntegerField(null=True),
        ),
    ]
