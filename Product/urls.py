from django.urls import path
from . import views
urlpatterns = [
    path('<slug:c>/',views.category,name='Category'),
    path('<int:tid>/<str:pid>/', views.product_detail,name='Product_Details'),
    path('add/<int:tid>/<str:pid>/', views.add_view,name='AddCart'),

]
