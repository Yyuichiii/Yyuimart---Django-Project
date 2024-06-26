# Generated by Django 5.0.1 on 2024-02-11 10:28

import Product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeadPhone',
            fields=[
                ('Brand', models.CharField(max_length=15, null=True)),
                ('PName', models.CharField(max_length=20, null=True, verbose_name='Product Name')),
                ('Description', models.TextField(null=True)),
                ('Price', models.PositiveBigIntegerField(null=True)),
                ('Quantity', models.IntegerField(null=True)),
                ('PID', models.CharField(default=Product.models.HeadPhone.format, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('PImage', models.ImageField(null=True, upload_to='HeadPhone', verbose_name='Product Image')),
            ],
            options={
                'ordering': ('PID',),
            },
        ),
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('Brand', models.CharField(max_length=15, null=True)),
                ('PName', models.CharField(max_length=20, null=True, verbose_name='Product Name')),
                ('Description', models.TextField(null=True)),
                ('Price', models.PositiveBigIntegerField(null=True)),
                ('Quantity', models.IntegerField(null=True)),
                ('PID', models.CharField(default=Product.models.Laptop.format, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('PImage', models.ImageField(null=True, upload_to='Laptop', verbose_name='Product Image')),
            ],
            options={
                'ordering': ('PID',),
            },
        ),
        migrations.CreateModel(
            name='Men',
            fields=[
                ('Brand', models.CharField(max_length=15, null=True)),
                ('PName', models.CharField(max_length=20, null=True, verbose_name='Product Name')),
                ('Description', models.TextField(null=True)),
                ('Price', models.PositiveBigIntegerField(null=True)),
                ('Quantity', models.IntegerField(null=True)),
                ('PID', models.CharField(default=Product.models.Men.format, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('PImage', models.ImageField(null=True, upload_to='Men', verbose_name='Product Image')),
            ],
            options={
                'ordering': ('PID',),
            },
        ),
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('Brand', models.CharField(max_length=15, null=True)),
                ('PName', models.CharField(max_length=20, null=True, verbose_name='Product Name')),
                ('Description', models.TextField(null=True)),
                ('Price', models.PositiveBigIntegerField(null=True)),
                ('Quantity', models.IntegerField(null=True)),
                ('PID', models.CharField(default=Product.models.Mobile.format, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('PImage', models.ImageField(null=True, upload_to='Mobile', verbose_name='Product Image')),
            ],
            options={
                'ordering': ('PID',),
            },
        ),
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('Brand', models.CharField(max_length=15, null=True)),
                ('PName', models.CharField(max_length=20, null=True, verbose_name='Product Name')),
                ('Description', models.TextField(null=True)),
                ('Price', models.PositiveBigIntegerField(null=True)),
                ('Quantity', models.IntegerField(null=True)),
                ('PID', models.CharField(default=Product.models.Shoe.format, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('PImage', models.ImageField(null=True, upload_to='Shoe', verbose_name='Product Image')),
            ],
            options={
                'ordering': ('PID',),
            },
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('Brand', models.CharField(max_length=15, null=True)),
                ('PName', models.CharField(max_length=20, null=True, verbose_name='Product Name')),
                ('Description', models.TextField(null=True)),
                ('Price', models.PositiveBigIntegerField(null=True)),
                ('Quantity', models.IntegerField(null=True)),
                ('PID', models.CharField(default=Product.models.Women.format, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('PImage', models.ImageField(null=True, upload_to='Women', verbose_name='Product Image')),
            ],
            options={
                'ordering': ('PID',),
            },
        ),
    ]
