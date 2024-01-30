from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# If someone wants to write every method of its own , they can inherit BaseUserManager from django.contrib.auth.base_user otherwise AbstractBaseUser
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, name , Phone):
        """
        Create and save a user with the given email password name and phone.
        """
        # if not email:
        #     raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,Phone=Phone)
        
        user.set_password(password)
        user.save()
        return user
  
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email password name and phone.
        """
        user = self.create_user(
            email,
            password=password,
            name="Admin",
            Phone=""
        )
        user.is_superuser = True
        user.is_staff= True
        user.save(using=self._db)
        return user
