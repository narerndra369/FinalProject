from django.urls import path
from . import views

urlpatterns = [
    
    path('restaurantsignin',views.restaurantsignin,name='restaurantsignin'),
    path('restaurantsignup',views.restaurantsignup,name='restaurantsignup'),
    path('addfood',views.addfood,name='addfood'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('addtables',views.addtables,name='addtables'),
    path('vieworders',views.vieworders,name='vieworders'),
    path('deletetable/<int:id>',views.deletetable,name='deletetable'),
    path('viewpayments',views.viewpayments,name="viewpayments"),
    path('viewordqr/<int:id>/',views.viewordqr,name="viewordqr"),
    path('sendpaymentreq/<int:id>/',views.sendpaymentreq,name="sendpaymentreq"),
    path('decodepayqr/<int:id>/',views.decodepayqr,name="decodepayqr"),
    path('complete/<int:id>/',views.complete,name="complete"),



]