from django.shortcuts import render,redirect
from .models import user_address,CustomUser,Cart,Order
from .forms import User_Reg,login_form,User_Change_Reg,custom_password_change,address_form,otp_form
from .email import password_email,order_recieved,email_otp,email_success_register
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from Product.models import Mobile,Laptop,HeadPhone,Men,Women,Shoe 
from django.views import View
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from User_Account.utils import generateOTP
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db import transaction





# Function to logout admin before visiting the webpages
def admin_logout(request):
    if(request.user.is_superuser):       #Condition to check if user is admin or not
            logout(request)                #Logout function in django.contrib.auth
            messages.success(request, "Admin has been logout !!!")

# Home
def home(request): 
    admin_logout(request)   #Function to logout the admin   
    product=Women.objects.all()   #Women Product Queryset 
    type=ContentType.objects.get_for_model(Women)  
    return render(request,'User_Account/home.html',{'product':product,'type':type})

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
                    # This email services can be delay and will not impact on the other services
                    email_success_register.delay(inactive_user.email,inactive_user.name)
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
             messages.success(request, "Profile has been updated !!!")
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
            password_email.delay(user.name,user.email)  # For activating the email service
            messages.success(request, "Password is changed Successfully !!!")
            return redirect('home')
    return render(request,'User_Account/changepassword.html',{'form':fm})


# Class based Address
class address(View):  

    def get(self,request):
        admin_logout(request)
        if(not request.user.is_authenticated):
            return redirect('login')
        
        # 
        address_querset=user_address.objects.filter(user=request.user)
        if not address_querset.exists():        
            fm=address_form()
        else:
            address_object=user_address.objects.get(user=request.user)
            
            initial_dict = { 
                'Name':address_querset[0].Name,
                'Phone':address_querset[0].Phone,
                'Pincode':address_querset[0].Pincode,
                'State':address_querset[0].State,
                'house_no':address_querset[0].house_no,
                'Road_name':address_querset[0].Road_name,
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
        


# User Cart
def cart_fun(request):   
    
    o=Cart.objects.filter(user=request.user)
    if not o.exists():
        messages.success(request,"Cart is Empty Please add Something first ")
        return redirect('home')
    else:
        total_price=0
        for item in o:
            total_price=total_price+item.Quantity*item.content_object.Price

        

        return render(request,"User_Account/cart.html",{'Products':o,'total_price':total_price})


# Function to delete the cart item
def delete(request,i):
    obj=Cart.objects.get(pk=i)
    obj.delete()
    messages.success(request,"The selected Item has delete successfully")
    return redirect('cart')

# Function to add the quantity of the product
def add(request,i):
    obj=Cart.objects.get(pk=i)
    obj.Quantity=obj.Quantity+1
    obj.save()
    
    messages.success(request,"The Quantity of the selected Item has been added successfully")
    return redirect('cart')

# Function to reduce the quantity of the product
def reducee(request,i):
    
    obj=Cart.objects.get(id=i)
    if obj.Quantity==1:
        return redirect('delete',i)
    obj.Quantity=obj.Quantity-1
    obj.save()

    messages.success(request,"The Quantity of the selected Item has been reduced successfully")
    return redirect('cart')

# Checkout 
def checkout(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None:
        return redirect('home')
    o=Cart.objects.filter(user=request.user)
    if not o.exists():
        return redirect('home')
    obj=user_address.objects.filter(user=request.user)
    m=""
    if not obj.exists():
        m="Address is Not Set"

    total_price=0
    for item in o:
        total_price=total_price+item.Quantity*item.content_object.Price

    return render(request,"User_Account/checkout.html",{'Address':obj,'m':m,'tp':total_price,"product":o})


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
    
    with transaction.atomic():
        cart_queryset = Cart.objects.filter(user=request.user)
        orders_to_create = []
        for obj in cart_queryset:
            order = Order(
                user=obj.user,
                content_type=obj.content_type,
                PID=obj.PID,
                Quantity=obj.Quantity,
                Category=obj.content_object.Category,
                Price=obj.content_object.Price * obj.Quantity,
                Address=obj.user.user_address
            )
            orders_to_create.append(order)
        
        # Bulk create orders
        order=Order.objects.bulk_create(orders_to_create)
        total_price = sum(obj.Price for obj in order)

        # Delete cart items
        cart_queryset.delete()

    # Email Services    
    order_recieved(order,request.user,total_price)
    messages.success(request, "Order has been Successfully Received ")
    return redirect("home")


# Orders Section
def orders(request):
    if not(request.user.is_authenticated):
        return redirect('home')
    
    obj = Order.objects.filter(user=request.user).order_by('-id').select_related('user','Address','content_type')

    paginator = Paginator(obj, 5)  # Show 5 orders per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "User_Account/orders.html", {"Products": page_obj})
    
