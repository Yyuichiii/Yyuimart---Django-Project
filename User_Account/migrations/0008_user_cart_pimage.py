# Generated by Django 4.2.5 on 2023-12-12 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Account', '0007_rename_categories_user_cart_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_cart',
            name='PImage',
            field=models.ImageField(null=True, upload_to='', verbose_name='Product Image'),
        ),
    ]