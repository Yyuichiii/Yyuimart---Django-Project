from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('login/', views.login_fun,name='login'),
    path('logout/', views.logout_fun,name='logout'),
    path('register/', views.registration,name='registration'),
    path('profile/', views.profile,name='profile'),
    path('orders/', views.orders,name='orders'),
    path('profile/address/', views.address.as_view(),name='address'),
    path('password_change/', views.password_change,name='password_change'),
    path('cart/', views.cart_fun,name='cart'),
    path('c/<int:i>', views.delete,name='delete'),
    path('d/<int:i>', views.add,name='add'),
    path('e/<int:i>', views.reducee,name='reduce'),
    path('cart/checkout/', views.checkout,name='checkout'),
    path('cart/checkout/edit_address', views.edit_address.as_view(),name='edit_address'),
    path('cart/checkout/success', views.success,name='success'),
    path('otp/', views.otpfun,name='otp'),
   
    
]
