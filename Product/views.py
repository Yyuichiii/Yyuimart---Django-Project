from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpResponseForbidden
from .models import Mobile,Laptop,HeadPhone,Men,Women,Shoe
from User_Account.models import cart
from django.contrib import messages

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


# def add_cart(request,pid):
    
#     c=cart(user=request.user,PID=pid,quantity=1)
#     c.save()
#     product_details(request,pid)
    

def add_cart(request):
    if(not request.user.is_authenticated):
        return HttpResponse(status=403)
    if request.method=="GET":
        a=request.GET["id"]
        



        # for adding mobiles in the cart
        if Mobile.objects.filter(PID=a).exists():
            
            b=Mobile.objects.get(PID=a)
            o=cart.objects.filter(user=request.user) & cart.objects.filter(ID_Mobile=b)
            if not o.exists():
                d=cart(user=request.user,ID_Mobile=b,Quantity=1)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q)

        # for adding Laptops in the cart
        if Laptop.objects.filter(PID=a).exists():
            
            b=Laptop.objects.get(PID=a)
            o=cart.objects.filter(user=request.user) & cart.objects.filter(ID_Laptop=b)
            if not o.exists():
                d=cart(user=request.user,ID_Laptop=b,Quantity=1)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q)


        # for adding Headphones in the cart
        if HeadPhone.objects.filter(PID=a).exists():
            
            b=HeadPhone.objects.get(PID=a)
            o=cart.objects.filter(user=request.user) & cart.objects.filter(ID_Headphone=b)
            if not o.exists():
                d=cart(user=request.user,ID_Headphone=b,Quantity=1)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q)


        # for adding Men in the cart
        if Men.objects.filter(PID=a).exists():
            
            b=Men.objects.get(PID=a)
            o=cart.objects.filter(user=request.user) & cart.objects.filter(ID_Men=b)
            if not o.exists():
                d=cart(user=request.user,ID_Men=b,Quantity=1)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q)


        # for adding Women in the cart
        if Women.objects.filter(PID=a).exists():
            
            b=Women.objects.get(PID=a)
            o=cart.objects.filter(user=request.user) & cart.objects.filter(ID_Women=b)
            if not o.exists():
                d=cart(user=request.user,ID_Women=b,Quantity=1)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q)


        # for adding Shoe in the cart
        if Shoe.objects.filter(PID=a).exists():
            
            b=Shoe.objects.get(PID=a)
            o=cart.objects.filter(user=request.user) & cart.objects.filter(ID_Shoe=b)
            if not o.exists():
                d=cart(user=request.user,ID_Shoe=b,Quantity=1)
                d.save()

            else:                
                q=o[0].Quantity+1
                o.update(Quantity=q)
 
        
        c1=0;
        if(request.user.is_authenticated):       
            obj=cart.objects.filter(user=request.user)
            for o in obj:
                c1=c1+o.Quantity   
        o=Mobile.objects.filter(PID=a)
        print(o) 


 
    return JsonResponse({'cart_no':c1})


def temp(request):
    if(not request.user.is_authenticated):
        return HttpResponse(status=403)
        if request.method=="GET":
            a=request.GET["id"]
            o=cart.objects.filter(user=request.user)
            if not o.exists():
                c=cart(user=request.user,ID_Mobile=a,Quantity=1)
                c.save()

