from django.urls import path
from . import views
urlpatterns = [
    path('<slug:c>/',views.category,name='Category'),
    path('category/<str:pid>/', views.product_details,name='Product_Details'),
    path('buynow/<str:pid>/', views.buy_now.as_view(),name='Buy_now'),
    path('addcart',views.add_cart_class.as_view(),name='addcart'),

]
