from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from Product.models import Mobile,Laptop,HeadPhone,Men,Women,Shoe
from django.core.validators import MaxValueValidator, MinValueValidator



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
    Name=models.CharField(max_length=30,blank=False,null=False)
    Phone=models.CharField(max_length=15,blank=False)
    Pincode=models.CharField(max_length=6,blank=False)
    State=models.CharField(max_length=20,blank=False)
    house_no=models.CharField(max_length=50,blank=False,null=False)
    Road_name=models.CharField(max_length=75,blank=False,null=False)

    def __str__(self):
        return f"{self.user}"
    

class cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    ID_Mobile=models.ForeignKey(Mobile,on_delete=models.CASCADE,blank=True,null=True)
    ID_Laptop=models.ForeignKey(Laptop,on_delete=models.CASCADE,blank=True,null=True)
    ID_Headphone=models.ForeignKey(HeadPhone,on_delete=models.CASCADE,blank=True,null=True)
    ID_Men=models.ForeignKey(Men,on_delete=models.CASCADE,blank=True,null=True)
    ID_Women=models.ForeignKey(Women,on_delete=models.CASCADE,blank=True,null=True)
    ID_Shoe=models.ForeignKey(Shoe,on_delete=models.CASCADE,blank=True,null=True)
    Quantity=models.PositiveIntegerField(default='0')



   