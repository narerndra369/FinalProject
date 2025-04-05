from django.db import models
from datetime import datetime
from django.conf.global_settings import TIME_ZONE  # importing time zone
# from django.utils.timezone import utc

current_time = datetime.now()

# Create your models here.


class Customerdetails(models.Model):
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Userqr(models.Model):
    restaurantid = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="True")

    def __str__(self):
        return self.restaurantid


class Tablebooking(models.Model):
    restaurantid = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    tableno = models.CharField(max_length=50)
    memberscount = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="pending")

    def __str__(self):
        return self.restaurantid

import os
class OrderItem(models.Model):
    """Order Item Model"""
    price = models.IntegerField(null=True)
    restaurent_id = models.CharField(max_length=100)
    dish_id = models.CharField(max_length=100)
    dish_count = models.CharField(max_length=100)
    table_number = models.CharField(max_length=100)
    dish_name = models.CharField(max_length=100)

    order = models.ForeignKey("Customer.Useroder", on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.price)


class Useroder(models.Model):
    """Order Model Containing Many OrderItems"""
    tablenumber = models.CharField(max_length=100, null=True)
    restaurent_id = models.CharField(max_length=100, null=True)
    user_email = models.EmailField(null=True)
    total_cost = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    qrcode = models.FileField(upload_to=os.path.join('static', 'order_qr_codes'), null=True)
    key = models.BinaryField(null=True)
    otp = models.IntegerField(null=True)
    order_status =  models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return self.user_email

class PaymentDetails(models.Model):
    tablenumber = models.CharField(max_length=100,null=True)    
    resid = models.CharField(max_length=100,null=True)
    Email = models.EmailField()
    cardname = models.CharField(max_length=100,null=True)
    cardno = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    expirydate = models.CharField(max_length=100)
    cvv = models.CharField(max_length=100)
    order_id = models.ForeignKey(Useroder, on_delete=models.CASCADE, null=True)
    qrcode = models.FileField(upload_to=os.path.join('static', 'order_qr_codes'), null=True)
    key = models.BinaryField(null=True)
    otp = models.IntegerField(null=True)



from django.utils import timezone

class WaitlingList(models.Model):
    """Waiting List Model"""
    time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    table_number = models.CharField(max_length=50)
    user_email = models.EmailField(null=True)

    @property
    def get_time(self):
        # Get the current time in UTC
        now = timezone.now()  # This gives the current time in UTC based on Django settings
        time_diff = now - self.time
        print(time_diff)
        diff = round(60 - (time_diff.total_seconds() / 60))
        return diff if diff > 0 else 0

    def __str__(self):
        return str(self.time)
