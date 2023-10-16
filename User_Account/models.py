from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class val(RegexValidator):
    message = _("Enter a valid Phone number.")


from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=30, blank=False)
    phoneNumberRegex = val(regex = r"^\+?1?\d{8,15}$")
    Phone = models.CharField(_("Phone"),validators = [phoneNumberRegex], max_length=15, blank=False) 
    
        

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


class user_address(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    Name=models.CharField(max_length=30,blank=False)
    Phone=models.CharField(max_length=15,blank=False)
    Pincode=models.CharField(max_length=6,blank=False)
    State=models.CharField(max_length=10,blank=False)
    house_no=models.CharField(max_length=25,blank=False)
    Road_name=models.CharField(max_length=30,blank=False)

    def __str__(self):
        return f"{self.user}"
