from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import User_Reg
from django.contrib.auth.models import User


# Test
def test(request):
    fm=User_Reg()
    if request.method=="POST":
        fm = User_Reg(request.POST)
        if fm.is_valid():                       
            fm.save()
            return redirect('home')


    return render(request,'cart/test.html',{'form':fm})


# Home
def home(request):
    return render(request,'cart/home.html')

# Login
def login(request):
    return render(request,'cart/login.html')

# Registration
def registration(request):
    fm=User_Reg()
    if request.method=="POST":
        fm = User_Reg(request.POST)
        if fm.is_valid():
                                   
            fm.save()
            return redirect('home')
    return render(request,'cart/customerregistration.html',{'form':fm})

# User Profile
def profile(request):
    return render(request,'cart/profile.html')

# User Password Change
def password_change(request):
    return render(request,'cart/changepassword.html')

# User Cart
def cart(request):   
    return render(request,'cart/addtocart.html')