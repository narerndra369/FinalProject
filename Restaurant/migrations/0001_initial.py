# Generated by Django 3.2.10 on 2023-05-12 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='qrcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurantid', models.CharField(max_length=100)),
                ('qrcode', models.CharField(max_length=100)),
                ('qrcodepath', models.CharField(max_length=100)),
                ('customeremail', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('restaurantname', models.CharField(max_length=100)),
                ('qrcode', models.CharField(max_length=100, null=True)),
                ('qrcodepath', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
