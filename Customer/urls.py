from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('customersignin',views.customersignin,name='customersignin'),
    path('customersignup',views.customersignup,name='customersignup'),
    path('viewrestaurants',views.viewrestaurants,name='viewrestaurants'),
    path('viewqr/<int:id>',views.viewqr,name='viewqr'),
    path('qr', views.Qrcode, name='qr'),
    path('tablebooking', views.tablebooking, name='tablebooking'),
    path('menu', views.menu, name='menu'),
    path('userorder',views.userorder,name="userorder"),
    path('save-order/', views.save_order, name='save_order'),
    path('payment/<int:id>/',views.payment,name="payment"),
    path('myorders',views.myorders,name="myorders"),
    path('waiting_list',views.waiting_list,name="waiting_list"),
    path('pay/<int:id>/',views.pay,name="pay"),
    path('check',views.check_waiting_list,name="check"),
]