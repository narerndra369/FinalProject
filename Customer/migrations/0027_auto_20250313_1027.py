# Generated by Django 3.2 on 2025-03-13 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0026_auto_20250311_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='useroder',
            name='restaurent_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='useroder',
            name='tablenumber',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
