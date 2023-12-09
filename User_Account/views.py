from django.shortcuts import render,redirect
from .models import user_address,cart
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .forms import User_Reg,login_form,User_Change_Reg,custom_password_change,address_form
from .email import registration_email,password_email,order_recieved
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from Product.models import Mobile,Laptop,HeadPhone,Men,Women,Shoe 
from itertools import chain
from django.core import serializers
from django.views import View


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
def cart_fun(request):   
    print("dsf")
    
    o=cart.objects.filter(user=request.user)
    if not o.exists():
        messages.success(request,"Cart is Empty Please add Something first ")
        return redirect('home')
    else:
        # Function defined below
        tp=total_Price(o) 

        return render(request,"User_Account/addtocart.html",{'Products':o,'Total_Price':tp})

# Function for calculating the total price in the cart
def total_Price(o):    
    tp=0
    for a in o:
        
        if a.ID_Mobile:
            tp=tp+a.Quantity*a.ID_Mobile.Price
        
        if a.ID_Laptop:
            tp=tp+a.Quantity*a.ID_Laptop.Price

        if a.ID_Headphone:
            tp=tp+a.Quantity*a.ID_Headphone.Price

        if a.ID_Men:
            tp=tp+a.Quantity*a.ID_Men.Price

        if a.ID_Women:
            tp=tp+a.Quantity*a.ID_Women.Price

        if a.ID_Shoe:
            tp=tp+a.Quantity*a.ID_Shoe.Price

    return tp


# Class based Address
class address(View):
    
    def get(self,request):
        admin_logout(request)
        if(not request.user.is_authenticated):
            return redirect('login')
        
        objj=user_address.objects.filter(user=request.user)
        if not objj.exists():
        
            fm=address_form()
        else:
            for obj in objj:
                initial_dict = { 
                    'Name':obj.Name,
                    'Phone':obj.Phone,
                    'Pincode':obj.Pincode,
                    'State':obj.State,
                    'house_no':obj.house_no,
                    'Road_name':obj.Road_name,
                } 
            fm=address_form(initial=initial_dict)

        return render(request,'User_Account/address.html',{'form':fm})
        

    def post(self,request):
        fm = address_form(request.POST)
        if fm.is_valid():
            obj=fm.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request, "Address has been successfully changed !!!")
            return redirect('profile')
        
# Function to logout admin before visiting the webpages
def admin_logout(request):
    if(request.user.is_superuser):
            logout(request)
            messages.success(request, "Admin has been logout !!!")

# Function to delete the cart item
def delete(request,i):
    obj=cart.objects.get(id=i)
    obj.delete()
    messages.success(request,"The selected Item has delete successfully")
    return redirect('cart')

# Function to add the quantity of the product
def add(request,i):
    obj=cart.objects.get(id=i)
    update=obj.Quantity+1
    
    obj.Quantity=update
    obj.save()
    
    messages.success(request,"The Quantity of the selected Item has been added successfully")
    return redirect('cart')

# Function to reduce the quantity of the product
def reducee(request,i):
    
    obj=cart.objects.get(id=i)
    if obj.Quantity==1:
        return redirect('delete',i)
    update=obj.Quantity-1
    obj.Quantity=update
    obj.save()

    messages.success(request,"The Quantity of the selected Item has been reduced successfully")
    return redirect('cart')

# Checkout 
def checkout(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None:
        return redirect('home')
    o=cart.objects.filter(user=request.user)
    if not o.exists():
        return redirect('home')
    obj=user_address.objects.filter(user=request.user)
    m=""
    if not obj.exists():
        m="Address is Not Set"

    
    tp=total_Price(o)+100
    return render(request,"User_Account/checkout.html",{'Address':obj,'m':m,'tp':tp,"product":o})


# Class based view for edit address in checkout
class edit_address(address):
    def post(self,request):
        fm = address_form(request.POST)
        if fm.is_valid():
            obj=fm.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request, "Address has been successfully changed !!!")
            return redirect('checkout')

# Order Placed Showed but orders are not saving and cart is deleting 

def success(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None:
        return redirect('home')
    obj=cart.objects.filter(user=request.user)
    obj.delete()
    order_recieved(email=request.user)
    messages.success(request,"Order has been Successfully Recevied ")
    return redirect("home")