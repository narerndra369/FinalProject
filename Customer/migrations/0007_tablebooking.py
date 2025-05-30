# Generated by Django 4.1.4 on 2023-05-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Customer", "0006_userqr"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tablebooking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("restaurantid", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=50)),
                ("tableno", models.CharField(max_length=50)),
                ("memberscount", models.CharField(max_length=50)),
                ("status", models.CharField(default="pending", max_length=50)),
            ],
        ),
    ]
