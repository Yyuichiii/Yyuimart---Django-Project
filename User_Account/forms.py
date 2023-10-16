from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django import forms 
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import CustomUser,user_address
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation



class User_Reg(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Enter the Password'}),label = "Password")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Re-Enter the Password'}),label = "Confirm Password")
    
    class Meta:
        model=CustomUser
        fields=['name','email','Phone','password1','password2',]
        labels={'email':'Email','name':'Name','Phone':'Phone Number'}
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter the Email'}),'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Name',}),'Phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Phone Number',})}
        


class User_Change_Reg(UserChangeForm):
    password=None
    class Meta:
        model=CustomUser
        fields=['name','Phone']
        labels={'name':'Name','Phone':'Phone Number'}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Name',}),'Phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Phone Number',})}
       

class login_form(forms.Form):
        
        email=forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control",'placeholder': 'Enter the Email',"autofocus": True}),label = "Email",required=True)
    
        password=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Enter the Password'}),label = "Password")

        error_messages = {
        "invalid_login": _(
            "Please enter the correct email/password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }
        def get_invalid_login_error(self):
            return ValidationError(self.error_messages["invalid_login"],code="invalid_login",)
        
        def clean(self):
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")

            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()

class custom_password_change(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class": "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),)
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class": "form-control"}),)

    old_password = forms.CharField(label=_("Old password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": True,"class": "form-control"}))


class address_form(forms.ModelForm):
    
    class Meta:
        model = user_address
        exclude = ('user',)
        # fields=['Name' ,'user','Phone','Pincode','State','house_no','Road_name']

        