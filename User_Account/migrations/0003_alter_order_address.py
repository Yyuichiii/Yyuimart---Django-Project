# Generated by Django 5.0.1 on 2024-02-11 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Account', '0002_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='User_Account.user_address'),
        ),
    ]
