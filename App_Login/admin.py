from django.contrib import admin
from App_Login.models import User, Profile, SellerInfo

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(SellerInfo)

