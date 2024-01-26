from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home,name='home'),
    path('register/', views.Register_view.as_view(),name='api_registration'),
    path('otp/<str:uid>/<str:token>/', views.Otp_view.as_view(),name='api_OTP'),
    path('login/', views.LoginView.as_view(),name='api_login'),
    path('logout/', views.LogoutView.as_view(),name='api_logout'),
    path('profile/', views.User_Profile.as_view(),name='api_profile'),
    # path('orders/', views.orders,name='orders'),
    ]