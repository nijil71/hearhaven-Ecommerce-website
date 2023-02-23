from django import forms

class ShopRegisterForm(forms.Form):
    shopname=forms.CharField( max_length=100)
    address=forms.CharField( max_length=100)
    email=forms.EmailField()
    phone=forms.IntegerField()
    password=forms.CharField( max_length=100)
    confirm_password=forms.CharField( max_length=100)

class ShopLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField( max_length=100)


class ProductUploadForm(forms.Form):
    productname=forms.CharField( max_length=100)
    productprice=forms.IntegerField()
    productdescription=forms.CharField( max_length=100)
    productimage=forms.ImageField()

class CardDetails(forms.Form):
    cardnumber=forms.CharField( max_length=100)
    cardname=forms.CharField( max_length=100)
    cardexpiry=forms.CharField( max_length=100)
    cardcvv=forms.CharField( max_length=100)