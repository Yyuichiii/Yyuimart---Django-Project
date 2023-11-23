from django.shortcuts import render
from django.http import HttpResponse
from .models import Mobile

def product_details(request,pid): 
    p=Mobile.objects.get(PID=pid)
    
    return render(request,'Product/productdetail.html',{'Product':p})

def category(request,c):
    if c=='Mobile':
        all_products=Mobile.objects.all()

    # if c=='Laptop':
    #     all_products=Laptop.objects.all()

        return render(request,'Product/categories.html',{'P':all_products})
