from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from HearHaven_site.settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate
from .forms import *
from .models import *
import os
import uuid
import datetime

# Create your views here.


def index(request):
    return render(request, 'shopurban.html')


def shopregister(request):
    if request.method == 'POST':
        form = ShopRegisterForm(request.POST)
        if form.is_valid():
            shopname = form.cleaned_data['shopname']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                return HttpResponse('Passwords do not match')
            else:
                data = ShopRegisterModel(
                    shopname=shopname,
                    address=address,
                    email=email,
                    phone=phone,
                    password=password,
                )
                data.save()
                # redirect - it is a function that is used to redirect to another function or url
                return redirect(shoplogin)
        else:
            return HttpResponse('Invalid Request')
    return render(request, 'shop_register.html')


def shoplogin(request):
    if request.method == 'POST':
        form = ShopLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            data = ShopRegisterModel.objects.all()
            # is used to make a variable global
            request.session['email'] = email
            for i in data:
                if i.email == email and i.password == password:
                    request.session['id'] = i.id
                    return redirect(profile_page)
            return HttpResponse('Invalid Credentials')
        else:
            return HttpResponse('Invalid Request')

    return render(request, 'shop_login.html')


def productupload(request):
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        id=request.session['id']
        if form.is_valid():
            productname = form.cleaned_data['productname']
            productprice = form.cleaned_data['productprice']
            productdescription = form.cleaned_data['productdescription']
            productimage = form.cleaned_data['productimage']
            data = ProductUploadModel(
                shopid=id,
                productname=productname,
                productprice=productprice,
                productdescription=productdescription,
                productimage=productimage,
            )
            data.save()
            return redirect(profile_page)

        else:
            return HttpResponse('Invalid Request')
    return render(request, 'product_upload.html')


def profile_page(request):
    shopname=request.session['email']
    return render(request, 'profile_page.html',{'shopname':shopname})


def productview(request):
    shpid=request.session['id']
    data = ProductUploadModel.objects.all()
    image = []
    name = []
    price = []
    description = []
    id = []
    shopid=[]
    for i in data:
        sid=i.shopid
        shopid.append(sid)
        ids = i.id
        id.append(ids)
        im = i.productimage
        image.append(str(im).split('/')[-1])
        name.append(i.productname)
        price.append(i.productprice)
        description.append(i.productdescription)
    mylist = zip(image, name, price, description, id,shopid)
    return render(request, 'product_view.html', {'mylist': mylist, 'shopid':shpid})


def view_all_products(request):
    data = ProductUploadModel.objects.all()
    image = []
    name = []
    price = []
    description = []
    id = []
    for i in data:
        ids = i.id
        id.append(ids)
        im = i.productimage
        image.append(str(im).split('/')[-1])
        name.append(i.productname)
        price.append(i.productprice)
        description.append(i.productdescription)
    mylist = zip(image, name, price, description, id)
    return render(request, 'view_all_products.html', {'mylist': mylist})



# what is crud?
# create,read,update,delete


def productdelete(request, id):
    data = ProductUploadModel.objects.get(id=id)
    data.delete()
    return redirect(productview)


def productedit(request, id):
    data = ProductUploadModel.objects.get(id=id)
    image = str(data.productimage).split('/')[-1]
    if request.method == 'POST':
        if len(request.FILES):  # to check whether the user has uploaded a new image or not
            if len(data.productimage) > 0:
                os.remove(data.productimage.path)
            data.productimage = request.FILES['productimage']
        data.productname = request.POST.get('productname')
        data.productprice = request.POST.get('productprice')
        data.productdescription = request.POST.get('productdescription')
        data.save()
        return redirect(productview)

    return render(request, 'product_edit.html', {'data': data, 'image': image})

# user model it is the default model used in django.It is basically used for authentication and authorization
# user model has 5 fields - 1.username,2.first_name,3.last_name,4.email,5.password


def send_mail_regis(email, auth_token):
    subject = 'Email Verification'
    message = f'Hi, Click on the link to verify your email http://127.0.0.1:8000/verify/{auth_token}'
    email_from = EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject, message, email_from, recipient)


def registeruser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # checking whether the username or email already exists
        if User.objects.filter(username=username).first():
            # messgae.success is a framework that allows you to store messages in one request and retrieve them in another request
            messages.success(request, 'Username already exists')
            return redirect(registeruser)

        if User.objects.filter(email=email).first():
            messages.success(request, 'Email already exists')
            return redirect(registeruser)

        user_obj = User(first_name=first_name, last_name=last_name,
                        username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        # uuid module is used to generate unique id
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(
            user=user_obj, auth_token=auth_token)
        profile_obj.save()
        # user defined
        send_mail_regis(email, auth_token)
        return render(request, 'success.html')
    return render(request, 'user_register.html')



def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        request.session['id'] = user_obj.id
        if user_obj is None:  # if username does not exist
            messages.success(request, 'username does not exist')
            return redirect(loginuser)
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:  # if not profile is verified
            messages.success(request, 'Email not verified')
            return redirect(loginuser)
        user = authenticate(username=username, password=password)
        # authenticate - it is a function that is used to verify a set of credentials.It take credential as keyword arguments,username and password for the default case check them and returns a user object
        if user is None:
            messages.success(request, 'Invalid credentials')
            return redirect(loginuser)


        request.session['username'] = username
        username = username.upper()
        # return redirect(userviewproduct)  
        return render(request, 'user_profile.html', {'username': username})
    
    return render(request, 'user_login.html')


def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'Email already verified')
            return redirect(loginuser)
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, 'YOur account has been verified')
        return redirect(loginuser)
    else:
        messages.success(request, 'user not found')
        return redirect(loginuser)


def userviewproduct(request):
    username = request.session['username']
    username = username.upper()

    data = ProductUploadModel.objects.all()
    image = []
    name = []
    price = []
    description = []
    id = []
    for i in data:
        ids = i.id
        id.append(ids)
        im = i.productimage
        image.append(str(im).split('/')[-1])
        name.append(i.productname)
        price.append(i.productprice)
        description.append(i.productdescription)
    mylist = zip(image, name, price, description, id)
    return render(request, 'user_view_products.html', {'mylist': mylist, 'username': username})

def addtocart(request, id):
    cartid=request.session['id']
    data = ProductUploadModel.objects.get(id=id)
    if Cart.objects.filter(productname=data.productname,userid=cartid).exists():
        return redirect(userviewproduct)
    else:

        save_to_cart = Cart(userid=cartid,productname=data.productname, productprice=data.productprice,
                            productdescription=data.productdescription, productimage=data.productimage)
        save_to_cart.save()
    return redirect(userviewproduct)


def showcart(request):
    uid=request.session['id']
    data = Cart.objects.all()
    image = []
    name = []
    price = []
    description = []
    id = []
    userids=[]
    for i in data:
        usid=i.userid
        userids.append(usid)
        ids = i.id
        id.append(ids)
        im = i.productimage
        image.append(str(im).split('/')[-1])
        name.append(i.productname)
        price.append(i.productprice)
        description.append(i.productdescription)
    mylist = zip(image, name, price, description, id,userids)
    return render(request, 'cart.html', {'mylist': mylist,'userid':uid})


def deletecart(request, id):
    data = Cart.objects.get(id=id)
    data.delete()
    return redirect(showcart)


def wishlist(request, id):
    wishid=request.session['id']
    data = ProductUploadModel.objects.get(id=id)
    if Wishlist.objects.filter(productname=data.productname,userid=wishid).exists():
        return redirect(userviewproduct)
    else:
        save_to_wishlist = Wishlist(userid=wishid,productname=data.productname, productprice=data.productprice,
                                    productdescription=data.productdescription, productimage=data.productimage)
        save_to_wishlist.save()
    return redirect(userviewproduct)


def deletewishlist(request, id):
    data = Wishlist.objects.get(id=id)
    data.delete()
    return redirect(showwishlist)


def showwishlist(request):
    uid=request.session['id']
    data = Wishlist.objects.all()
    image = []
    name = []
    price = []
    description = []
    id = []
    userids=[]
    for i in data:
        usid=i.userid
        userids.append(usid)
        ids = i.id
        id.append(ids)
        im = i.productimage
        image.append(str(im).split('/')[-1])
        name.append(i.productname)
        price.append(i.productprice)
        description.append(i.productdescription)
    mylist = zip(image, name, price, description, id,userids)
    return render(request, 'wishlist.html', {'mylist': mylist,'userid':uid})

def wishlisttocart(request, id):
    wishid=request.session['id']
    data = Wishlist.objects.get(id=id)
    if Cart.objects.filter(productname=data.productname,userid=wishid).exists():
        return redirect(showwishlist)
    else:
        save_to_cart = Cart(userid=wishid,productname=data.productname, productprice=data.productprice,
                            productdescription=data.productdescription, productimage=data.productimage)
        save_to_cart.save()
    return redirect(showwishlist)

def cartbuy(request, id):
    data = Cart.objects.get(id=id)
    image = str(data.productimage).split('/')[-1]
    if request.method == 'POST':
        name = request.POST.get('productname')
        price = request.POST.get('productprice')
        quantity = request.POST.get('productquantity')
        save_order = Buy(productname=name, productprice=price,
                         quantity=quantity)
        save_order.save()
        total = int(price)*int(quantity)
        return render(request, 'finalbill.html', {'total': total, 'name': name, 'price': price, 'quantity': quantity, 'image': image})
    return render(request, 'cartbuy.html', {'data': data, 'image': image})


def send_mail_orderconfirmed(email):
    subject = 'Order Confirmed'
    message = f'Hi, Your order has been confirmed. Your order will be delivered within 3-4 days. Thank you for shopping with us.'
    email_from = EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject, message, email_from, recipient)


def carddetails(request):
    if request.method == 'POST':
        cardnumber = request.POST.get('cardnumber')
        cardname = request.POST.get('cardname')
        cardcvv = request.POST.get('cardcvv')
        cardexpiry = request.POST.get('cardexpiry')
        save_card = CardDetailsModel(
            cardnumber=cardnumber, cardname=cardname, cardcvv=cardcvv, cardexpiry=cardexpiry)
        save_card.save()
        today = datetime.date.today()
        deliverydate = today+datetime.timedelta(days=10)
        return render(request, 'orderstatus.html', {'deliverydate': deliverydate})
    return render(request, 'card_details.html')

def usernotification(request):
    data=UserNotification.objects.all()
    return render(request,'usernotif.html',{'data':data})


def shopnotification(request):
    data=ShopNotification.objects.all()
    return render(request,'shopnotif.html',{'data':data})