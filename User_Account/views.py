from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import User_Reg
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

# Send Email
def send_email(name,email):
    subject = 'Welcome to Yyuicart !!!'
    message = 'Hi '+name+' thank you for creating account in Yyuicart.\n\nHope you have a good day ahead'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )




# Test
def test(request):
    fm=User_Reg()
    if request.method=="POST":
        fm = User_Reg(request.POST)
        if fm.is_valid():                       
           
            send_email()
            fm.save()
            messages.success(request, "Account has been successfully created !!!")
            

            return redirect('login')


    return render(request,'User_Account/test.html',{'form':fm})


# Home
def home(request):  
    # messages.success(request, "Account has been successfully created !!!")
    return render(request,'User_Account/home.html')

# Login
def login(request):
    return render(request,'User_Account/login.html')

# Registration
def registration(request):
    fm=User_Reg()
    if request.method=="POST":
        fm = User_Reg(request.POST)
        if fm.is_valid():
            uemail=fm.cleaned_data['email']                                   
            uname=fm.cleaned_data['name']                                   
            fm.save()
            send_email(uname,uemail)
            messages.success(request, "Account has been successfully created !!!")
            return redirect('login')
    return render(request,'User_Account/customerregistration.html',{'form':fm})

# User Profile
def profile(request):
    return render(request,'User_Account/profile.html')

# User Password Change
def password_change(request):
    return render(request,'User_Account/changepassword.html')

# User Cart
def cart(request):   
    return render(request,'User_Account/addtocart.html')