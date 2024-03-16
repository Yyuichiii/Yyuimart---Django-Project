from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotFound,HttpResponse
from .models import Mobile,Laptop,HeadPhone,Men,Women,Shoe
from User_Account.models import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


def category(request, c):
    category_model_mapping = {
        'Mobile': Mobile,
        'Laptop': Laptop,
        'HeadPhone': HeadPhone,
        'Men': Men,
        'Women': Women,
        'Shoe': Shoe,
    }

    # Check if the category is valid
    if c in category_model_mapping:
        category_model = category_model_mapping[c]
        type=ContentType.objects.get_for_model(category_model)
        all_products = category_model.objects.all()
        return render(request, 'Product/categories.html', {'P': all_products,'type':type})

    else:
        # Handle invalid category here
        all_products = []

    return render(request, 'Product/categories.html', {'P': all_products})


def product_detail(request,tid,pid):
    try:
        type=ContentType.objects.get_for_id(tid)
        p=type.get_object_for_this_type(PID=pid)
        return render(request,'Product/productdetail.html',{'Product':p,'type':type})
    except:
        return HttpResponseNotFound("Product not found.")

@login_required
def add_view(request,tid,pid):
    
        if Cart.objects.filter(PID=pid ,user=request.user).exists():
            cart_obj=Cart.objects.get(PID=pid,user=request.user)
            cart_obj.Quantity=cart_obj.Quantity+1
            cart_obj.save()
        else:
            content_type=ContentType.objects.get_for_id(tid)
            cart=Cart.objects.create(
                user=request.user,
                content_type=content_type,
                PID=pid,
            )
            cart.save()

        c=Cart.objects.filter(user=request.user).aggregate(cart_no=Sum('Quantity'))
        return HttpResponse({c['cart_no']})
    