from django.contrib import admin
from App_Order.models import Cart, Order, Coupon

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Coupon)

