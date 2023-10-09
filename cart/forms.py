from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms 


class User_Reg(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Enter the Password'}),label = "Password")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Re-Enter the Password'}),label = "Confirm Password")
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter the Email'}),'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Username'})}
        


