from threading import Thread
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
import os
import random
from django.http import JsonResponse
import json
from datetime import datetime
import time


from django.db.models import Q
# Create your views here.
from Restaurant.models import *
from .models import Customerdetails, PaymentDetails
from Restaurant .models import Restaurant, qrcode
from .models import Userqr, Customerdetails, Tablebooking, Useroder, WaitlingList, OrderItem

JOB_RUN_TIME = 1000 * 10

_INDEXPAGE = 'index.html'
_CUSTOMERSIGNINPAGE = 'customersignin.html'
_CUSTOMERSIGNUPPAGE = 'customersignup.html'
_CUSTOMERHOMEPAGE = 'customerhome.html'
_VIEWRESTAURANTSPAGE = 'viewrestaurants.html'
_VIEWQRPAGE = 'viewqr.html'
_INPUTFIELDPAGE = 'inputfield.html'
_TABLEBOOKINGPAGE = 'tablebooking.html'
_MENUPAGE = 'menu.html'
_USERORDERPAGE = "userorder.html"
_PAYMENTPAGE = "payment.html"
file_path = os.path.join(os.getcwd(), "email.txt")


def index(req):
    print("Hello")
    return render(req, _INDEXPAGE)


def customersignin(req):
    if req.method == "POST":
        email = req.POST["useremail"]
        password = req.POST["password"]
        data = Customerdetails.objects.filter(
            email=email, password=password).exists()
        if data:
            req.session['email'] = email
            email = req.session.get('email')
            return render(req, _CUSTOMERHOMEPAGE)
        else:
            messages.info(req, "Invalid credentials")
            return render(req, _CUSTOMERSIGNINPAGE)
    return render(req, _CUSTOMERSIGNINPAGE)


def customersignup(req):
    if req.method == "POST":
        first = req.POST["first"]
        last = req.POST["last"]
        email = req.POST["email"]
        password = req.POST["password"]
        confirm_password = req.POST["confirm_password"]
        if password == confirm_password:
            data = Customerdetails.objects.filter(
                email=email, password=password).exists()
            if data:
                messages.info(req, "Email already exists")
                return render(req, _CUSTOMERSIGNUPPAGE, {"first": first})
            dc = Customerdetails(first=first, last=last,
                                 email=email, password=password)
            dc.save()
            messages.info(req, "User created")
            return render(req, _CUSTOMERSIGNINPAGE, {"first": first})
        return render(req, _CUSTOMERSIGNUPPAGE)
    return render(req, _CUSTOMERSIGNUPPAGE)


def viewrestaurants(req):
    dc = Restaurant.objects.all()
    return render(req, _VIEWRESTAURANTSPAGE, {'dc': dc})


def viewqr(req, id):
    q = Userqr.objects.filter(
        restaurantid=id, email=req.session['email']).exists()
    if q:
        try:
            dq = Userqr.objects.filter(
                restaurantid=id, email=req.session['email'], status="True").exists()
            if dq:
                return render(req, _INPUTFIELDPAGE, {"res_id": id})
            else:
                dc = Userqr(restaurantid=id, email=req.session['email'])
                dc.save()
                with open(file_path, "w+") as f:
                    f.write(req.session['email'])
                data = Restaurant.objects.filter(id=id)
                return render(req, _VIEWQRPAGE, {'dc': data})
        except Exception as e:
            print(e)
    dc = Userqr(restaurantid=id, email=req.session['email'])
    dc.save()
    data = Restaurant.objects.filter(id=id)
    return render(req, _VIEWQRPAGE, {'dc': data})
def Qrcode(req):
    try:
        id = req.GET['id']
        with open(file_path, "r+") as f:
            email = f.read()
        if Userqr.objects.filter(restaurantid=id, email=email, status="True").exists():
            return HttpResponse("You can view the menu now.")

        q = Userqr.objects.get(restaurantid=id, email=email)
        q.status = "True"
        q.save()
        return HttpResponse("You can view the menu now.")
    except Exception as e:
        print(e)
        return HttpResponse("Sorry We are facing some Technical Issues")


def tablebooking(req):
    if req.method == "POST":
        memberscount = req.POST["memberscount"]
        res_id = req.POST["res_id"]
        req.session['rid'] = res_id
        available_tables = tables.objects.filter(
            memberscount=memberscount, status='available')
        table_numbers = tables.objects.filter(
            memberscount=memberscount, status='available').values_list('tableno')
        if available_tables.count() > 0:
            random_table_number = random.choice([i for i in table_numbers])
            reserved_table = random_table_number[0]
            updated_table = tables.objects.get(tableno=reserved_table)
            updated_table.status = "reserved"
            updated_table.save()
            dc = addfoodinfo.objects.filter(restaurantid=res_id)
            return render(req, _MENUPAGE, {'data': dc, "rid": res_id, "tableno": reserved_table, "total": dc.count()})
        elif tables.objects.filter(memberscount=memberscount, status='reserved').count() > 0:
            random_tables = tables.objects.filter(
                memberscount=memberscount, status='reserved').values_list('tableno')
            random_table_number = random.choice([i for i in random_tables])
            reserved_table = random_table_number[0]
            waiting_list = WaitlingList(count=memberscount,
                                        table_number=reserved_table,
                                        user_email=req.session['email']
                                        )
            waiting_list.save()
            req.session['members_count'] = memberscount
            return redirect('waiting_list')
        else:
            return HttpResponse("Tables Are Not Available In The Selected Restaurant")
    return render(req, _TABLEBOOKINGPAGE)

def check_waiting_list(req):
    waiting_list = WaitlingList.objects.all()

    for item in waiting_list:
        if item.get_time == 0:
            # getting the items user_email and table number
            table_number = item.table_number
            user_email = item.user_email
            table = tables.objects.get(tableno=table_number)
            table.status = "reserved"
            table.memberscount = item.count
            table.user_email = user_email

            item.delete()
    
    return HttpResponse("Checked Waitling List")



def waiting_list(req):
    
    filtered_list = WaitlingList.objects.filter(
        count=req.session['members_count'])
    return render(req, _TABLEBOOKINGPAGE, {"waiting_list": filtered_list,   "current_time": datetime.now()})


def menu(req):
    data = addfoodinfo.objects.filter(restaurantid=req.session['rid'])


    dc = WaitlingList.objects.filter(user_email= req.session['email']).values_list("table_number").last()[0]
    print("======")
    print(dc)
    return render(req, _MENUPAGE, {'data': data,
                                   "total": data.count(),
                                   "tableno": dc,
                                   "restaurantid": req.session['rid'],
                                   "rid":req.session['rid']
                                   })


import json
import qrcode
from io import BytesIO
from django.http import JsonResponse, HttpRequest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .aes import *
from django.core.mail import send_mail

def userorder(req: HttpRequest):
    if req.method == "POST":
        body = json.loads(req.body)
        dishes: list[str] = body['dishes']
        dishes_count: list[int] = body['dishes_count']
        Tableno = body['tableno']
        restaurantid = body['restaurantid']
        user_email = req.session.get("email", "")  # Safely get the user's email from the session
        total_price = 0
        print(user_email)

        # Create a new order in the Useroder model
        dc = Useroder(user_email=user_email)
        dc.save()

        order_details = {
            "order_id": dc.id,
            "table_number": Tableno,
            "restaurant_id": restaurantid,
            "total_price": 0,
            "items": []
        }

        # Loop through dishes to store each item in the order
        for i in range(len(dishes)):
            dish_id = dishes[i]
            dish = addfoodinfo.objects.get(id=dish_id)
            
            order_item = OrderItem(
                price=dish.foodprice,
                restaurent_id=restaurantid,
                dish_count=dishes_count[i],
                dish_id=dish_id,
                table_number=Tableno,
                dish_name=dish.foodname,
                order_id=dc.id
            )
            order_item.save()

            # Add item details to the order
            total_price += int(dish.foodprice) * int(dishes_count[i])

            order_details["items"].append({
                "dish_name": dish.foodname,
                "dish_count": dishes_count[i],
                "price_per_item": dish.foodprice,
                "total_item_price": int(dish.foodprice) * int(dishes_count[i])
            })

        # Update the total cost of the order
        dc.total_cost = total_price
        dc.save()
        order_details["total_price"] = total_price

        readable_order_details = f"Order ID: {dc.id}\nTable: {Tableno}\nRestaurant: {restaurantid}\n\nItems:\n"
        for item in order_details["items"]:
            readable_order_details += f"{item['dish_name']} x{item['dish_count']} - {item['total_item_price']} ({item['price_per_item']} each)\n "
        readable_order_details +=f'Total Price: {total_price}\n'
        # Generate the QR code for the order details
        qr = qrcode.make(readable_order_details)
        qr_io = BytesIO()
        qr.save(qr_io, format="PNG")
        qr_io.seek(0)  # Move to the start of the BytesIO object

        # Save the QR code to Django's media storage
        qr_path = f"static/order_qr_codes/order_{dc.id}.png"
        default_storage.save(qr_path, ContentFile(qr_io.getvalue()))
        
        # Get the URL of the saved QR code image
        qr_url = default_storage.url(qr_path)
        print(qr_path)
        print(qr_url)
        key = get_random_bytes(32)  # AES 256-bit key

        enc_path = aes_encrypt(qr_path, key)
        otp =random.randint(100000, 999999)
        # Save the QR code path in the Useroder model
        dc.restaurent_id = restaurantid
        dc.tablenumber = Tableno
        dc.qrcode = enc_path
        dc.key=key
        dc.otp = otp
        dc.save()
        rest = Restaurant.objects.get(id=restaurantid)
        # Send the email to the restaurant with the OTP for unlocking the QR code details
        email_subject = 'New Order - QR Code Access OTP'
        email_message = f'''Hello {rest.restaurantname},

We have received a new order from the customer at table number {Tableno}.

Order details:
Order ID: {dc.id}
Total Price: {total_price}
Items: {', '.join([item['dish_name'] for item in order_details['items']])}

To view and unlock the order details, use the following OTP:
OTP: {otp}  # You can use the key or generate OTP here, depending on how you plan to handle it

Please use this OTP to decrypt the QR code and access the complete details.

Best regards,
Your Restaurant Team
'''

        send_mail(
            email_subject,
            email_message,
            'narendramalapula123@gmail.com',  # The email you are sending from
            [user_email],  # The restaurant's email
            fail_silently=False,
        )



        # Return the success response with the QR code URL
        return JsonResponse({
            "msg": "Successfully added order",
            "url": "myorders",  # This is where you can redirect the user after order is created
            "qr_code_url": qr_url  # Include the URL of the generated QR code
        })




def myorders(req):
    data = Useroder.objects.filter(user_email=req.session['email'])
    print(data, req.session['email'])
    # dataone = OrderItem.objects.filter(order_id=data.id)
    return render(req, _USERORDERPAGE, {'data': data})


def save_order(request):
    if request.method == 'POST' and request.is_ajax():
        order_data = request.POST.get('order_data')
        print(order_data)
        # Process and store the order_data in the database

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Order placed successfully'})
    else:
        # Return a JSON response indicating an error
        return JsonResponse({'error': 'Invalid request'})


def payment(req, id):
    data = Useroder.objects.get(id=id)
    # dataone = OrderItem.objects.all().last()
    return render(req, _PAYMENTPAGE, {'id':id,"total": data.total_cost,'restaurent_id':data.restaurent_id,'tableno':data.tablenumber})


def pay(req, id):
    if req.method == "POST":
        tablenumber= req.POST['tablenumber']
        resid = req.POST['resid']
        useremail = req.session['email']
        print(useremail)
        namecard = req.POST['namecard']
        cardno = req.POST['cardno']
        amount = req.POST['amount']
        expirydate = req.POST['expirydate']
        cvv = req.POST['cvv']
        order =  Useroder.objects.get(id=id)
        dc = PaymentDetails(tablenumber=tablenumber,resid=resid,Email=useremail, cardname=namecard,
                            cardno=cardno, amount=amount, expirydate=expirydate, cvv=cvv)
        dc.save()
        paymentdetails = f"Payment_ID: {dc.id}\n Order_ID: {id}\n Restaurent_ID: {resid}\n Table_Number: {tablenumber}\n Piad_By: {useremail}\n Name_On_Card: {namecard}\n Total_Amount:{amount}\n Order_Status: Paid\n"
        qr = qrcode.make(paymentdetails)
        qr_io = BytesIO()
        qr.save(qr_io, format="PNG")
        qr_io.seek(0)  # Move to the start of the BytesIO object

        # Save the QR code to Django's media storage
        qr_path = f"static/Payment_qr_codes/Payment_{dc.id}.png"
        default_storage.save(qr_path, ContentFile(qr_io.getvalue()))
        
        # Get the URL of the saved QR code image
        qr_url = default_storage.url(qr_path)
        # print(qr_path)
        # print(qr_url)
        key = get_random_bytes(32)  # AES 256-bit key

        enc_path = aes_encrypt(qr_path, key)
        otp =random.randint(100000, 999999)
        order.order_status = "Paid"
        order.save()
        dc.qrcode = enc_path
        dc.key=key
        dc.otp = otp
        dc.order_id=order
        dc.save()
        rest = Restaurant.objects.get(id=resid)
        email_subject = 'New Payment - QR Code Access OTP'
        email_message = f'''Hello {rest.restaurantname},

We have successfully processed a payment for the new order from the customer at table number {tablenumber}.

Order details:
Order ID: {dc.id}
Total Price: {amount}


The payment has been successfully completed. To view and unlock the order details, use the following OTP:
OTP: {otp}

Please use this OTP to decrypt the QR code and access the complete details.

Best regards,
Your Restaurant Team
'''
        send_mail(
            email_subject,
            email_message,
            'narendramalapula123@gmail.com',  # The email you are sending from
            [useremail],  # The restaurant's email
            fail_silently=False,
        )



    
        messages.info(req, "Payment Process Completed Successfully")
        dc = Restaurant.objects.all()
        return render(req, _VIEWRESTAURANTSPAGE, {'dc': dc})
    return redirect("viewrestaurants")
