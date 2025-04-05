from django.urls import path
from . import views

urlpatterns = [
    
    path('adminsignin',views.adminsignin,name='adminsignin'),
    path('adminrestaurants',views.adminrestaurants,name='adminrestaurants'),
    path('adminusers',views.adminusers,name='adminusers'),
    path('adminorders',views.adminorders,name="adminorders"),
   
]