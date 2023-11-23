from django.urls import path
from . import views
urlpatterns = [
    path('<slug:c>/',views.category,name='Category'),
    path('mobile/<str:pid>', views.product_details,name='Product_Details'),
    # path('login/', views.login_fun,name='login'),
    # path('logout/', views.logout_fun,name='logout'),
    # path('register/', views.registration,name='registration'),
    # path('profile/', views.profile,name='profile'),
    # path('profile/address/', views.address,name='address'),
    # path('password_change/', views.password_change,name='password_change'),
    # path('cart/', views.cart,name='cart'),
    
]
