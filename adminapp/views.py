from django.shortcuts import render
from Restaurant.models import Restaurant 
from Customer.models import Customerdetails,OrderItem
# Create your views here.
def adminsignin(req):
    if req.method=="POST":
        useremail = req.POST['useremail']
        password = req.POST['password']
        if useremail=="admin@gmail.com" and password=="admin":
            return render(req,"adminhome.html",{'name':'Admin'})
    return render(req,"adminsignin.html")

def adminrestaurants(req):
    all_restaurants = Restaurant.objects.all()
    return render(req,"adminrestaurants.html",{'all_restaurants':all_restaurants})

def adminusers(req):
    all_users = Customerdetails.objects.all()
    return render(req,"adminusers.html",{'all_users':all_users})

def adminorders(req):
    all_orders = OrderItem.objects.all()
    return render(req,"adminorders.html",{'all_orders':all_orders})