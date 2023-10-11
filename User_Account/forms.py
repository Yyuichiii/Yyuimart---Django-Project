from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django import forms 


class User_Reg(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Enter the Password'}),label = "Password")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",'placeholder': 'Re-Enter the Password'}),label = "Confirm Password")
    
    class Meta:
        model=CustomUser
        fields=['name','email','Phone','password1','password2',]
        labels={'email':'Email','name':'Name','Phone':'Phone Number'}
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter the Email'}),'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Name',}),'Phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Phone Number',})}
        


class User_Change_Reg(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=['first_name']