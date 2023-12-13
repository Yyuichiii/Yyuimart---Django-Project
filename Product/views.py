from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpResponseForbidden
from .models import Mobile,Laptop,HeadPhone,Men,Women,Shoe
from User_Account.models import User_cart
from django.contrib import messages
from django.views import View

def product_details(request,pid): 
    
    cid=pid[:1]
    if cid=='M':
        cid=pid[:2]
        if cid=="MF":
            p=Men.objects.get(PID=pid)
        else:
            p=Mobile.objects.get(PID=pid)

    if cid=='L':
        p=Laptop.objects.get(PID=pid)

    if cid=='H':
        p=HeadPhone.objects.get(PID=pid)

    if cid=='W':
        p=Women.objects.get(PID=pid)


    if cid=='S':
        p=Shoe.objects.get(PID=pid)

    
    return render(request,'Product/productdetail.html',{'Product':p})

def category(request,c):
    if c=='Mobile':
        all_products=Mobile.objects.all()

    if c=='Laptop':
        all_products=Laptop.objects.all()

    if c=='HeadPhone':
        all_products=HeadPhone.objects.all()

    if c=='Men':
        all_products=Men.objects.all()

    if c=='Women':
        all_products=Women.objects.all()

    if c=='Shoe':
        all_products=Shoe.objects.all()

    return render(request,'Product/categories.html',{'P':all_products})


# Method to add products in the cart
class add_cart_class(View):
    def get(self,request):
        print("yeh waala chala")
        if(not request.user.is_authenticated):
            return HttpResponse(status=403)
        
        a=request.GET["id"]
        
        # for adding mobiles in the cart
        if Mobile.objects.filter(PID=a).exists():
            
            b=Mobile.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Mobile",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)

        # for adding Laptops in the cart
        if Laptop.objects.filter(PID=a).exists():
            
            b=Laptop.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Laptop",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Headphones in the cart
        if HeadPhone.objects.filter(PID=a).exists():
            
            b=HeadPhone.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="HeadPhone",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Men in the cart
        if Men.objects.filter(PID=a).exists():
            
            b=Men.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Men",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Women in the cart
        if Women.objects.filter(PID=a).exists():
            
            b=Women.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Women",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Shoe in the cart
        if Shoe.objects.filter(PID=a).exists():
            
            b=Shoe.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Shoe",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)
 
        
        c1=0;
        if(request.user.is_authenticated):       
            obj=User_cart.objects.filter(user=request.user)
            for o in obj:
                c1=c1+o.Quantity   
        
 
        return JsonResponse({'cart_no':c1})


class buy_now(View):
    def get(self, request,*args, **kwargs):
        for key,value in kwargs.items():
            a=value

        print(a)
        if Mobile.objects.filter(PID=a).exists():
            
            b=Mobile.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Mobile",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)

        # for adding Laptops in the cart
        if Laptop.objects.filter(PID=a).exists():
            
            b=Laptop.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Laptop",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Headphones in the cart
        if HeadPhone.objects.filter(PID=a).exists():
            
            b=HeadPhone.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="HeadPhone",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Men in the cart
        if Men.objects.filter(PID=a).exists():
            
            b=Men.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Men",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Women in the cart
        if Women.objects.filter(PID=a).exists():
            
            b=Women.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Women",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)


        # for adding Shoe in the cart
        if Shoe.objects.filter(PID=a).exists():
            
            b=Shoe.objects.get(PID=a)
            o=User_cart.objects.filter(user=request.user) & User_cart.objects.filter(PID=a)
            if not o.exists():
                d=User_cart(user=request.user,Quantity=1,Brand=b.Brand,PName=b.PName,Price=b.Price*1,PID=a,Category="Shoe",PImage=b.PImage)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q,Price=b.Price*q)
 
        return redirect("checkout")

