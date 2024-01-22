from django.shortcuts import render,redirect
from .models import user_address,CustomUser,User_cart,Order
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .forms import User_Reg,login_form,User_Change_Reg,custom_password_change,address_form,otp_form
from .email import password_email,order_recieved,email_otp,email_success_register
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from Product.models import Mobile,Laptop,HeadPhone,Men,Women,Shoe 
from django.views import View
from datetime import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from User_Account.utils import generateOTP


# Function to logout admin before visiting the webpages
def admin_logout(request):
    if(request.user.is_superuser):       #Condition to check if user is admin or not
            logout(request)                #Logout function in django.contrib.auth
            messages.success(request, "Admin has been logout !!!")

# Home
def home(request): 
    admin_logout(request)   #Function to logout the admin   
    product=Women.objects.all()   #Women Product Queryset   
    return render(request,'User_Account/home.html',{'product':product})

# Registration
def registration(request):
    if request.method=='GET':
        admin_logout(request)
        if(request.user.is_authenticated):
            return redirect('home')
        request.session.flush()


        fm=User_Reg()    
        #if request is get then empty form is initialized
    if request.method=="POST":
        fm = User_Reg(request.POST)     #if request is post
        if fm.is_valid():               #Check for Validations  
            # fm data is stored in session so otp verification can be done
            # fm.save() will save the form data and will create the user because fm is a user modelform 
            obj=fm.save(commit=False)
            obj.is_active=False
            obj.save()
            token=PasswordResetTokenGenerator().make_token(user=obj)
            uid= urlsafe_base64_encode(force_bytes(obj.id))
            return redirect('otp',uid=uid,token=token)
            

    return render(request,'User_Account/customerregistration.html',{'form':fm},status=200)

# Function for OTP VERIFICATION
def otpfun(request,uid,token):
  
    if request.method=='GET':
        try:
            fm=otp_form()
            otp_generated=str(generateOTP(6))
            user=CustomUser.objects.get(id=urlsafe_base64_decode(force_str(uid)))
        
            request.session['otp_generated']=otp_generated     #otp is stored in session

            email_otp(otp_generated,user.email,user.name)
            return render(request,'User_Account/otp.html',{'form':fm,'uid':uid,'token':token},status=200)
        except:
            return redirect('home')
    if request.method=='POST':
        
        fm=otp_form(request.POST)
        if fm.is_valid():
            otp_user=fm.cleaned_data['otp_digit']
            if request.session['otp_generated']==str(otp_user):
                inactive_user=CustomUser.objects.get(id=urlsafe_base64_decode(force_str(uid)))
                if PasswordResetTokenGenerator().check_token(user=inactive_user,token=token):
                    inactive_user.is_active=True
                    inactive_user.save()
                    email_success_register(inactive_user.email,inactive_user.name)
                    request.session.flush()
                    messages.success(request, "Account has been successfully created !!!")

                    return redirect('login')
            
                else:
                    inactive_user.delete()
                    messages.error(request, "The OTP Verification Process has been Expired. Please Register again !!!")
                    return redirect('registration')
            

            else:            
                messages.error(request, "OTP Incorrect. Try Again !!!")
                return render(request,'User_Account/otp.html',{'form':fm,'uid':uid,'token':token})
          

# Login
def login_fun(request):    
    admin_logout(request)
   
    if(request.user.is_authenticated):
        return redirect('home')
    request.session.flush()
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
    
    o=User_cart.objects.filter(user=request.user)
    if not o.exists():
        messages.success(request,"Cart is Empty Please add Something first ")
        return redirect('home')
    else:

        tp=0
        for a in o:
            tp=tp+a.Price


        return render(request,"User_Account/cart.html",{'Products':o,'Total_Price':tp})

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
        

# Function to delete the cart item
def delete(request,i):
    obj=User_cart.objects.get(id=i)
    obj.delete()
    messages.success(request,"The selected Item has delete successfully")
    return redirect('cart')

# Function to add the quantity of the product
def add(request,i):
    obj=User_cart.objects.get(id=i)
    update=obj.Quantity+1

    price=obj.Price/obj.Quantity
    
    obj.Quantity=update
    obj.Price=price*update
    obj.save()
    
    messages.success(request,"The Quantity of the selected Item has been added successfully")
    return redirect('cart')

# Function to reduce the quantity of the product
def reducee(request,i):
    
    obj=User_cart.objects.get(id=i)
    if obj.Quantity==1:
        return redirect('delete',i)
    update=obj.Quantity-1

    price=obj.Price/obj.Quantity

    obj.Quantity=update
    obj.Price=price*update
    obj.save()

    messages.success(request,"The Quantity of the selected Item has been reduced successfully")
    return redirect('cart')

# Checkout 
def checkout(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None:
        return redirect('home')
    o=User_cart.objects.filter(user=request.user)
    if not o.exists():
        return redirect('home')
    obj=user_address.objects.filter(user=request.user)
    m=""
    if not obj.exists():
        m="Address is Not Set"

    tp=0
    for a in o:
        tp=tp+a.Price

    tp=tp+100       #Added Shipping Charges
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
    
    tp=0
    obj=User_cart.objects.filter(user=request.user)
    for o in obj:
        tp=tp+o.Price
        Order.objects.create(user=request.user,PID=o.PID,Category=o.Category,Brand=o.Brand,PName=o.PName,Price=o.Price,Quantity=o.Quantity,PImage=o.PImage)
        
# Email Service temporarily Stopped    
    order_recieved(obj,request.user,tp+100)
    obj.delete()
    messages.success(request,"Order has been Successfully Recevied ")
    return redirect("home")


# Orders Section
def orders(request):
    if not(request.user.is_authenticated):
        return redirect('home')
    
    obj=Order.objects.filter(user=request.user).order_by('-id')
    
    return render(request,"User_Account/orders.html",{'Products':obj})