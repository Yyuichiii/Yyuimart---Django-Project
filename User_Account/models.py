from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .managers import CustomUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    
class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    PID = models.CharField(max_length=10)
    content_object = GenericForeignKey("content_type", "PID")
    Quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.PID




class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Order_time=models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    PID = models.CharField(max_length=10)
    content_object = GenericForeignKey("content_type", "PID")
    Quantity=models.PositiveIntegerField(default=1)
    Category=models.CharField(max_length=15,null=True)
    Price=models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return self.Category





   