# Generated by Django 4.1.4 on 2023-05-19 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Restaurant", "0007_alter_restaurant_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="tables",
            name="user_email",
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
