# Generated by Django 3.2.10 on 2023-05-12 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0002_addfood'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='addfood',
            new_name='addfoodinfo',
        ),
    ]
