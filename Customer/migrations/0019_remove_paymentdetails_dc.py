# Generated by Django 4.1.4 on 2023-05-19 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Customer", "0018_paymentdetails_cardname"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymentdetails",
            name="dc",
        ),
    ]
