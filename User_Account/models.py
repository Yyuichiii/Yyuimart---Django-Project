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
    name = models.CharField(_("name"), max_length=150, blank=False)
    phoneNumberRegex = val(regex = r"^\+?1?\d{8,15}$")
    Phone = models.CharField(_("Phone"),validators = [phoneNumberRegex], max_length=15, blank=False) 
    
        

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    

    objects = CustomUserManager()

    def __str__(self):
        return self.email