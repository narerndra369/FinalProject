from django.db import models
# import uuid

# Create your models here.
class Restaurant(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    restaurantname = models.CharField(max_length=100)
    qrcode = models.CharField(max_length=100,null=True)
    qrcodepath = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.restaurantname
    


class qrcode(models.Model):
    restaurantid = models.CharField(max_length=100)
    restaurantname = models.CharField(max_length=100,null=True)
    qrcode = models.CharField(max_length=100)
    qrcodepath = models.CharField(max_length=100)
    customeremail = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.restaurantid



class addfoodinfo(models.Model):
    restaurantid = models.CharField(max_length=100)
    foodname = models.CharField(max_length=100)
    foodprice = models.CharField(max_length=100)
    def __str__(self):
        return self.restaurantid
    

class tables(models.Model):
    restaurantid = models.CharField(max_length=100)
    memberscount = models.CharField(max_length=100)
    tableno = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default="available")
    user_email = models.EmailField(null=True)
    
    def __str__(self):
        return self.restaurantid
    

    