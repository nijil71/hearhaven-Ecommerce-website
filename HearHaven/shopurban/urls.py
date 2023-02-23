from django.urls import path
from .views import *

urlpatterns = [
    path('', index,name='index'),
    path('shopregister/', shopregister,name='shopregister'),
    path('shoplogin/', shoplogin,name='shoplogin'),
    path('productupload/', productupload),
    path('profile_page/', profile_page),
    path('productview/', productview,name='productview'),
    path('delete/<int:id>', productdelete,name='productdelete'),
    path('edit/<int:id>', productedit,name='productedit'),
    path('userregister/', registeruser,name='userregister'),
    path('userlogin/', loginuser,name='userlogin'),
    path('verify/<auth_token>', verify),
    path('viewproduct',userviewproduct,name='userviewproduct'),
    path('viewallproduct',view_all_products,name='userviewallproduct'),
    path('addtocart/<int:id>',addtocart),
    path('addtowishlist/<int:id>',wishlist,name='wishlist'),
    path('cart/',showcart,name='cart'),
    path('wishlist/',showwishlist,name='wishlist'),
    path('deletecart/<int:id>',deletecart),
    path('deletewishlist/<int:id>',deletewishlist),
    path('cartbuy/<int:id>',cartbuy),
    path('wishtocart/<int:id>',wishlisttocart,name='wishtocart'),
    path('card/',carddetails,name='card'),
    path('usernotif/',usernotification),
    path('shopnotif/',shopnotification)
]
