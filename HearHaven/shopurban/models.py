from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShopRegisterModel(models.Model):
    shopname=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    password=models.CharField(max_length=100)
    # The str method that returns human readable or informal string representraion of an object 
    def __str__(self):
        return self.shopname
        

class ShopLoginModel(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.email

class ProductUploadModel(models.Model):
    shopid=models.IntegerField()
    productname=models.CharField(max_length=100)
    productprice=models.IntegerField()
    productdescription=models.CharField(max_length=100)
    productimage=models.ImageField(upload_to='HearHaven/static')
    def __str__(self):
        return self.productname


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100,default=None,null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    userid=models.IntegerField()
    productname=models.CharField(max_length=100)
    productprice=models.IntegerField()
    productdescription=models.CharField(max_length=100)
    productimage=models.ImageField()
    def __str__(self):
        return self.productname

class Wishlist(models.Model):
    userid=models.IntegerField()
    productname=models.CharField(max_length=100)
    productprice=models.IntegerField()
    productdescription=models.CharField(max_length=100)
    productimage=models.ImageField()
    def __str__(self):
        return self.productname
    
class Buy(models.Model):
    productname=models.CharField(max_length=100)
    productprice=models.IntegerField()
    productdescription=models.CharField(max_length=100)
    productimage=models.ImageField()
    quantity=models.IntegerField()

class CardDetailsModel(models.Model):
    cardnumber=models.CharField( max_length=100)
    cardname=models.CharField( max_length=100)
    cardexpiry=models.CharField( max_length=100)
    cardcvv=models.CharField( max_length=100)
    def __str__(self):
        return self.cardname

class UserNotification(models.Model):
    content=models.CharField(max_length=100)
    notifdate=models.DateField(auto_now_add=True)

class ShopNotification(models.Model):
    content=models.CharField(max_length=100)
    notifdate=models.DateField(auto_now_add=True)