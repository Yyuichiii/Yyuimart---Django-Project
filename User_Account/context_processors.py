from .models import Cart
from django.db.models import Sum

# This is the context which will be available for every html render page throughout the project
def user_cart(request):
    c=0;
    if(request.user.is_authenticated):       
      cart=Cart.objects.filter(user=request.user).aggregate(cart_no=Sum('Quantity'))
      c=cart['cart_no']
      if c==None:
         c=0  

    return {'cart_no': c}

