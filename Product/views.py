from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseNotFound
from .models import Mobile,Laptop,HeadPhone,Men,Women,Shoe
from User_Account.models import User_cart
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        all_products = category_model.objects.all()
    else:
        # Handle invalid category here
        all_products = []

    return render(request, 'Product/categories.html', {'P': all_products})

def product_details(request,pid): 
    try:
        if pid.startswith('M'):
            if pid.startswith('MF'):
                p=Men.objects.get(PID=pid)
            else:
                p=Mobile.objects.get(PID=pid)

        if pid.startswith('L'):
            p=Laptop.objects.get(PID=pid)

        if pid.startswith('H'):
            p=HeadPhone.objects.get(PID=pid)

        if pid.startswith('W'):
            p=Women.objects.get(PID=pid)

        if pid.startswith('S'):
            p=Shoe.objects.get(PID=pid)
    
        return render(request,'Product/productdetail.html',{'Product':p})
    
    except:
        return HttpResponseNotFound("Product not found.")


# Method to add products in the cart
# class add_cart_class(View):
    def get(self,request):

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

class Common_Cart_BuyNow:
    def add_to_cart(self, request, product_model, pid):
        # Retrieve product details
        product = product_model.objects.get(PID=pid)
        # Check if the product is already in the user's cart
        cart_item = User_cart.objects.filter(user=request.user, PID=pid).first()

        if cart_item:
            # If the product is already in the cart, update quantity and price
            cart_item.Quantity += 1
            cart_item.Price += product.Price
            cart_item.save()
        else:
            # If the product is not in the cart, create a new cart item
            User_cart.objects.create(
                user=request.user,
                Quantity=1,
                Brand=product.Brand,
                PName=product.PName,
                Price=product.Price,
                PID=pid,
                Category=product.__class__.__name__,
                PImage=product.PImage
            )

        return
    
@method_decorator(login_required, name='dispatch')
class add_cart_class(Common_Cart_BuyNow, View):
    def get(self, request):
        pid = request.GET.get("id")

        # Check if the product is a Mobile
        if Mobile.objects.filter(PID=pid).exists():
            product_model = Mobile
        # Check if the product is a Laptop
        elif Laptop.objects.filter(PID=pid).exists():
            product_model = Laptop
        # Check if the product is a HeadPhone
        elif HeadPhone.objects.filter(PID=pid).exists():
            product_model = HeadPhone
        # Check if the product is a Men's product
        elif Men.objects.filter(PID=pid).exists():
            product_model = Men
        # Check if the product is a Women's product
        elif Women.objects.filter(PID=pid).exists():
            product_model = Women
        # Check if the product is a Shoe
        elif Shoe.objects.filter(PID=pid).exists():
            product_model = Shoe
        else:
            # Product not found
            return JsonResponse({'cart_no': 0})

        # Add product to cart and get total items
        self.add_to_cart(request, product_model, pid)
        
        # Calculate total items in the cart
        c1=0
        obj=User_cart.objects.filter(user=request.user)
        for o in obj:
            c1=c1+o.Quantity

        return JsonResponse({'cart_no': c1})
    

class buy_now(Common_Cart_BuyNow,View):
    def get(self, request, pid):
        if(not request.user.is_authenticated):
            messages.error(request, "Login to continue... !!!")
            return redirect(request.META.get('HTTP_REFERER'))
        
        # Check if the product is a Mobile
        if Mobile.objects.filter(PID=pid).exists():
            product_model = Mobile
        # Check if the product is a Laptop
        elif Laptop.objects.filter(PID=pid).exists():
            product_model = Laptop
        # Check if the product is a HeadPhone
        elif HeadPhone.objects.filter(PID=pid).exists():
            product_model = HeadPhone
        # Check if the product is a Men's product
        elif Men.objects.filter(PID=pid).exists():
            product_model = Men
        # Check if the product is a Women's product
        elif Women.objects.filter(PID=pid).exists():
            product_model = Women
        # Check if the product is a Shoe
        elif Shoe.objects.filter(PID=pid).exists():
            product_model = Shoe

        self.add_to_cart(request, product_model, pid)
    
        return redirect("checkout")
