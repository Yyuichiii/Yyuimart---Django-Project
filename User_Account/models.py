from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from Product.models import Mobile,Laptop,HeadPhone,Men,Women,Shoe
from .managers import CustomUserManager

# Custom validator for Phone number field
class val(RegexValidator):
    message = _("Enter a valid Phone number.")


# This is a custom user model inhertited from AbstractUser
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=30, blank=False)
    phoneNumberRegex = val(regex = r"^\+?1?\d{8,15}$")
    Phone = models.CharField(_("Phone"),validators = [phoneNumberRegex], max_length=15, blank=False) 
    
        
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
   
    objects = CustomUserManager()       #Custom User Model Manager

    def __str__(self):
        return self.email
    

class user_address(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    Name=models.CharField(max_length=30,blank=False,null=False)
    Phone=models.CharField(max_length=15,blank=False)
    Pincode=models.CharField(max_length=6,blank=False)
    State=models.CharField(max_length=20,blank=False)
    house_no=models.CharField(max_length=50,blank=False,null=False)
    Road_name=models.CharField(max_length=75,blank=False,null=False)

    def __str__(self):
        return f"{self.user}"
    


class User_cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    PID=models.CharField(max_length=5,null=True)
    Category=models.CharField(max_length=15,null=True)
    Brand=models.CharField(max_length=15,null=True)
    PName=models.CharField(max_length=20,null=True,verbose_name='Product Name')
    Price=models.PositiveBigIntegerField(null=True)
    Quantity=models.IntegerField(null=True)
    PImage=models.ImageField(null=True,verbose_name='Product Image')



class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Order_time=models.DateTimeField()
    PID=models.CharField(max_length=5,null=True)
    Category=models.CharField(max_length=15,null=True)
    Brand=models.CharField(max_length=15,null=True)
    PName=models.CharField(max_length=20,null=True,verbose_name='Product Name')
    Price=models.PositiveBigIntegerField(null=True)
    Quantity=models.IntegerField(null=True)
    PImage=models.ImageField(null=True,verbose_name='Product Image')




   