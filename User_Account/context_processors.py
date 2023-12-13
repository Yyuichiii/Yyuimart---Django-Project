from .models import User_cart

# This is the context which will be available for every html render page throughout the project
def user_cart(request):
    c=0;
    if(request.user.is_authenticated):       
      obj=User_cart.objects.filter(user=request.user)
      for o in obj:
          c=c+o.Quantity
    return {'cart_no': c}

