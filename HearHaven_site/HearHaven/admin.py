from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ShopRegisterModel)
admin.site.register(ShopLoginModel)
admin.site.register(ProductUploadModel)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Buy)
admin.site.register(CardDetailsModel)
admin.site.register(UserNotification)
admin.site.register(ShopNotification)

