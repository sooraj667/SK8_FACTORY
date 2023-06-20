from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . models import *
# Register your models here.


class CustomersAdmin(admin.ModelAdmin):
    list_display=("username","name","phonenumber","email")
class CategoryAdmin(admin.ModelAdmin):
    list_display=("name",)
class ProductsAdmin(admin.ModelAdmin):
    list_display=("name","price","quantity","category")
class OrdersAdmin(admin.ModelAdmin):
    list_display=("user","product","orderdate")
class CartAdmin(admin.ModelAdmin):
    list_display=("product","user","quantity")
class AddressAdmin(admin.ModelAdmin):
    list_display=("customer","country","state","district","locality","house","pincode")
class CouponAdmin(admin.ModelAdmin):
    list_display=("code","discount_percentage","isavailable")
class ProductofferAdmin(admin.ModelAdmin):
    list_display=("product","offer_description","discount")
class CategoryofferAdmin(admin.ModelAdmin):
    list_display=("category","offer_description","discount")
class WishlistAdmin(admin.ModelAdmin):
    list_display=("product","user")
class WalletAdmin(admin.ModelAdmin):
    list_display=("user","amount")
    





admin.site.register(Customers,CustomersAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Products,ProductsAdmin)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Productoffer,ProductofferAdmin)
admin.site.register(Categoryoffer,CategoryofferAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Wallet,WalletAdmin)
admin.site.register(Ordernumber)


