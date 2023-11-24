from django.shortcuts import render,redirect
from .models import user_address
from django.http import HttpResponse
from .forms import User_Reg,login_form,User_Change_Reg,custom_password_change,address_form
from .email import registration_email,password_email
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from Product.models import Mobile,Laptop,HeadPhone,Men,Women,Shoe 

# Home
def home(request): 
    admin_logout(request) 
    product=Women.objects.all()
    return render(request,'User_Account/home.html',{'product':product})

# Login
def login_fun(request):    
    admin_logout(request)
   
    if(request.user.is_authenticated):
        return redirect('home')
    fm=login_form()
    if request.method=="POST":
        fm = login_form(request.POST)
        if fm.is_valid():
            uemail=fm.cleaned_data['email'] 
            upas=fm.cleaned_data['password']
            user = authenticate(email=uemail,password=upas)
            if user is not None:
                login(request,user)
                addreess=user_address(user=request.user)
                addreess.save()
                messages.success(request, "Login Successfully !!!")
                return redirect('home')
            
                
            
    return render(request,'User_Account/login.html',{'form':fm})

# Logout
def logout_fun(request):
    logout(request)
    messages.success(request, "Logout Successfully !!!")
    return redirect('login')


# Registration
def registration(request):
    admin_logout(request)
    if(request.user.is_authenticated):
        return redirect('home')
    fm=User_Reg()
    if request.method=="POST":
        fm = User_Reg(request.POST)
        if fm.is_valid():
            uemail=fm.cleaned_data['email']                                   
            uname=fm.cleaned_data['name']                                   
            fm.save()
            registration_email(uname,uemail)                        
            messages.success(request, "Account has been successfully created !!!")
            return redirect('login')
    return render(request,'User_Account/customerregistration.html',{'form':fm})

# User Profile
def profile(request):
    admin_logout(request)
    if(not request.user.is_authenticated):
        return redirect('login')
    fm=User_Change_Reg(initial={'name': request.user.name,'Phone':request.user.Phone})
    if request.method == 'POST':
        fm = User_Change_Reg(request.POST,instance=request.user)
        if fm.is_valid():
             fm.save()
             return redirect('home')

    return render(request,'User_Account/profile.html',{'form':fm})

# User Password Change
def password_change(request):
    admin_logout(request)
    if(not request.user.is_authenticated):
        return redirect('login')
    fm=custom_password_change(request.user)
    if request.method == 'POST':

        fm = custom_password_change(request.user, request.POST)
        if fm.is_valid():
            user = fm.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            # password_email(user.name,user.email)  # For activating the email service
            messages.success(request, "Password is changed Successfully !!!")
            return redirect('home')
    return render(request,'User_Account/changepassword.html',{'form':fm})

# User Cart
def cart(request):   
    return render(request,'User_Account/addtocart.html')


# Address
def address(request):
    admin_logout(request)
    if(not request.user.is_authenticated):
        return redirect('login')
    
    obj=user_address.objects.get(user=request.user)

    initial_dict = { 
        'Name':obj.Name,
        'Phone':obj.Phone,
        'Pincode':obj.Pincode,
        'State':obj.State,
        'house_no':obj.house_no,
        'Road_name':obj.Road_name,
    } 
    fm=address_form(initial=initial_dict)
    if request.method == 'POST':
        fm = address_form(request.POST)
        if fm.is_valid():
            obj=fm.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request, "Address has been successfully changed !!!")
            return redirect('profile')
    return render(request,'User_Account/address.html',{'form':fm})


# Function to logout admin before visiting the webpages
def admin_logout(request):
    if(request.user.is_superuser):
            logout(request)
            messages.success(request, "Admin has been logout !!!")