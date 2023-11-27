from .models import cart

def user_cart(request):
    c=0;
    if(request.user.is_authenticated):       
      obj=cart.objects.filter(user=request.user)
      for o in obj:
          c=c+o.Quantity
    return {'cart_no': c}

