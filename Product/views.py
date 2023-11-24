from django.shortcuts import render
from django.http import HttpResponse
from .models import Mobile,Laptop,HeadPhone,Men,Women,Shoe

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
