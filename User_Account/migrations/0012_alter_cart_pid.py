# Generated by Django 5.0.1 on 2024-02-10 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Account', '0011_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='PID',
            field=models.CharField(max_length=10),
        ),
    ]
