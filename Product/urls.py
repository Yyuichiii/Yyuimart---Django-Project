from django.urls import path
from . import views
urlpatterns = [
    path('<slug:c>/',views.category,name='Category'),
    path('category/<str:pid>/', views.product_details,name='Product_Details'),
    path('addcart',views.add_cart,name='addcart'),

]
