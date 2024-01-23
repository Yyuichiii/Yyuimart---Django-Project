from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home,name='home'),
    path('register/', views.Register_view.as_view(),name='api_registration'),
    path('otp/<str:uid>/<str:token>/', views.Otp_view.as_view(),name='api_OTP'),
    # path('login/', views.login_fun,name='login'),
    # path('logout/', views.logout_fun,name='logout'),
    # path('profile/', views.profile,name='profile'),
    # path('orders/', views.orders,name='orders'),
    ]