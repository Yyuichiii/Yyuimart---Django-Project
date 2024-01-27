from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home,name='home'),
    path('register/', views.Register_view.as_view(),name='api_registration'),
    path('otp/<str:uid>/<str:token>/', views.Otp_view.as_view(),name='api_OTP'),
    path('login/', views.LoginView.as_view(),name='api_login'),
    path('refresh/', views.Refresh_token_view.as_view(),name='api_refreshtoken'),
    path('profile/', views.User_Profile.as_view(),name='api_profile'),
    path('address/', views.User_Address_View.as_view(),name='api_address'),
    path('password_change/', views.PasswordChangeView.as_view(),name='api_password_change'),
    # path('orders/', views.orders,name='orders'),
    ]