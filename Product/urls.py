from django.urls import path
from . import views
urlpatterns = [
    path('<slug:c>/',views.category,name='Category'),
    path('<int:tid>/<str:pid>/', views.product_detail,name='Product_Details'),
    path('Add_cart', views.add_to_cart,name='Add_to_Cart'),

]
