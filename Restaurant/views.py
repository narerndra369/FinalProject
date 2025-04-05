from django.shortcuts import render,redirect
import pyqrcode
from .models import Restaurant,qrcode,addfoodinfo,tables
from Customer.models import PaymentDetails,OrderItem
from django.http import HttpResponse, HttpRequest

from django.contrib import messages
public_ip = "localhost"
import random
import string
import os
alphabet = string.ascii_uppercase




_RESTAURANTSIGNINPAGE = 'restaurantsignin.html'
_RESTAURANTSIGNUPPAGE = 'restaurantsignup.html'
_RESTAURANTHOMEPAGE = 'restauranthome.html'
_ADDFOODPAGE = 'addfood.html'
_ADDTABLESPAGE = 'addtables.html'
_VIEWORDERSPAGE = 'vieworders.html'
_VIEWPAYMENTSPAGE = 'viewpayments.html'
file_path = os.path.join(os.getcwd() , "email.txt")

def restaurantsignin(req):
    if req.method=="POST":
        email = req.POST["useremail"]
        password = req.POST["password"]
        data = Restaurant.objects.filter(email=email,password=password).exists()
        if data:
            req.session['restaurantemail']=email
            q = Restaurant.objects.filter(email=email)[0]
            print(q)
            return render(req,_RESTAURANTHOMEPAGE,{'email':email})
        else:
            messages.info(req,"Invalid credentials")
            return render(req,_RESTAURANTSIGNUPPAGE)
    return render(req,_RESTAURANTSIGNINPAGE)

def restaurantsignup(req):
    if req.method=="POST":
        firstname = req.POST["first"]
        lastname = req.POST["last"]
        email = req.POST["email"]
        password = req.POST["password"]
        confirm_password = req.POST["confirm_password"]
        restaurantname = req.POST["rname"]
        if password==confirm_password:
            dc = Restaurant.objects.filter(email=email).exists()
            if dc:
                messages.info(req,"Email already exists")
                return redirect("restaurantsignup")
            data = Restaurant(firstname=firstname,lastname=lastname,email=email,password=password,restaurantname=restaurantname)
            data.save()
            q = Restaurant.objects.filter(email=email)[0]
            id = q.id
            useremail = q.email
            q.save()
            
            urls = f"http://{public_ip}:8000/qr?id={id}"
            url = pyqrcode.create(urls)
            url.png(f'static/qrcodes/{restaurantname}.png', scale=6)
            dc = Restaurant.objects.get(email=email)
            dc.qrcodepath = f'static/qrcodes/{restaurantname}.png'
            dc.qrcode = restaurantname+'.png'
            dc.save()
            dc = Restaurant.objects.filter(email=email).values_list('id', flat=True)
            print("12345678910")
            print(dc)



            data = qrcode(restaurantid=dc,qrcode=restaurantname+'.png',qrcodepath='static/qrcodes/'+restaurantname+'.png',restaurantname=restaurantname)
            data.save()
            messages.info(req,"User created")
            return redirect("restaurantsignin")
        else:
            messages.info(req,"Password not matching")
            return render(req,_RESTAURANTSIGNUPPAGE)
    return render(req,_RESTAURANTSIGNUPPAGE)


def addfood(req):
    dc = Restaurant.objects.filter(email=req.session['restaurantemail']).values_list('id', flat=True)
    restaurantid = dc[0]
    if req.method=="POST":
        dish = req.POST["dish"]
        amount = req.POST["amount"]
        dc = addfoodinfo(restaurantid=restaurantid,foodname=dish,foodprice=amount)
        dc.save()
        dc= addfoodinfo.objects.filter(restaurantid=restaurantid)
        return render(req,_ADDFOODPAGE,{'data':dc})
    dc= addfoodinfo.objects.filter(restaurantid=restaurantid)
    return render(req,_ADDFOODPAGE,{'data':dc})


def delete(req,id):
    dishid = id
    print(dishid)
    addfoodinfo.objects.filter(id=dishid).delete()
    return redirect('addfood')


def addtables(req):
    dc = Restaurant.objects.filter(email=req.session['restaurantemail']).values_list('id', flat=True)
    restaurantid = dc[0]
    if req.method == "POST":
        dc = Restaurant.objects.filter(email=req.session['restaurantemail']).values_list('id', flat=True)
        restaurantid = dc[0]
        members = req.POST["members"]
        count = int(req.POST["count"])
        # Based on count assign table numbers
        for i in range(1,count + 1):
            dc = tables(restaurantid=restaurantid,memberscount=members)
            dc.save()
            dc.refresh_from_db()
            dc.tableno = f'T{dc.id}'
            dc.save()
        dc = tables.objects.filter(restaurantid=restaurantid)
        return render(req,_ADDTABLESPAGE,{'data':dc})
    dc = tables.objects.filter(restaurantid=restaurantid)
    return render(req,_ADDTABLESPAGE,{'data':dc})


def deletetable(req,id):
    tableid = id
    print(tableid)
    tables.objects.filter(id=tableid).delete()
    return redirect('addtables')
from Customer.models import *
def vieworders(req):
    print(req.session['rid'])
    if Useroder.objects.filter(restaurent_id=req.session['rid']).exists():
        dc = Useroder.objects.filter(restaurent_id=req.session['rid'])
        return render(req,_VIEWORDERSPAGE,{'dc':dc})
    else:
        return HttpResponse("Orders not placed yet")


from Customer.aes import *
def viewordqr(req, id):
    print('hello')
    # dc = Restaurant.objects.filter(restaurent_id=req.session['rid'])
    if req.method == 'POST':
        otp1 = req.POST["otp1"]
        otp2 = req.POST["otp2"]
        otp3 = req.POST["otp3"]
        otp4 = req.POST["otp4"]
        otp5 = req.POST["otp5"]
        otp6 = req.POST["otp6"]
        print(otp1,otp2,otp3,otp4,otp5,otp6)
        otp = otp1+otp2+otp3+otp4+otp5+otp6
        data = Useroder.objects.get(id=id)

        if int(otp) == data.otp:
            encrypted_qr_path = data.qrcode.name  # This will give the file path as a string
            print(encrypted_qr_path)
            # Remove the 'static/order_qr_codes/' from the encrypted QR code path
            # encrypted_qr_path = encrypted_qr_path.replace('static/order_qr_codes/', '')

            # Decrypt the QR code path using the key
            qr_path = aes_decrypt(encrypted_qr_path, data.key)
            print(qr_path)
            # Append 'static/order_qr_codes/' back after decryption to get the full path
            # qr_path_with_static = f"static/order_qr_codes/{qr_path}"

            # Return the path to the template
            return render(req, 'orderqr.html', {'data': qr_path, 'id': id})
        else:
            return HttpResponse("Invalid OTP")
        # print(dc)
    return render(req, 'vieworderqr.html',{'id':id})


def sendpaymentreq(request, id):
    data = Useroder.objects.get(id=id)
    data.order_status = 'Accepted'
    data.save()
    return redirect('vieworders')

def viewpayments(req):
    # dataone = OrderItem.objects.filter(restaurent_id=req.session['rid'])
    try:
        data = PaymentDetails.objects.filter(resid=req.session['rid'])
        return render(req,_VIEWPAYMENTSPAGE,{'data':data})
    except:
        return HttpResponse("Payment not done yet")
    
def decodepayqr(req, id):
    data = PaymentDetails.objects.get(id=id)
    if req.method == 'POST':
        otp1 = req.POST["otp1"]
        otp2 = req.POST["otp2"]
        otp3 = req.POST["otp3"]
        otp4 = req.POST["otp4"]
        otp5 = req.POST["otp5"]
        otp6 = req.POST["otp6"]
        print(otp1,otp2,otp3,otp4,otp5,otp6)
        otp = otp1+otp2+otp3+otp4+otp5+otp6
        if int(otp) == int(data.otp):
            encrypted_qr_path = data.qrcode.name  # This will give the file path as a
            print(encrypted_qr_path)
            # Remove the 'static/order_qr_codes/' from the encrypted QR code path
            # encrypted_qr_path = encrypted_qr_path.replace('static/order_qr_codes/', '')
            # Decrypt the QR code path using the key
            qr_path = aes_decrypt(encrypted_qr_path, data.key)
            print(qr_path)
            # Append 'static/order_qr_codes/' back after decryption to get the full path
            qr_path_with_static = f"static/Payment_qr_codes/{qr_path}"
            print(qr_path_with_static, 'pjsbfsdjd')
            # Return the path to the template
            return render(req, 'viewpaydetails.html',{'data':qr_path,'id':id})
        else:
        
            return HttpResponse("Invalid OTP")
    return render(req, 'decodepayqr.html',{'id':id})


def complete(request, id):
    data = PaymentDetails.objects.get(id=id)
    data.order_id.order_status = 'Completed'
    data.save()
    return redirect('viewpayments')