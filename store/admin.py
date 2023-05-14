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
# class ProductImagesAdmin(admin.ModelAdmin):
#     list_display=("product","image")
class OrdersAdmin(admin.ModelAdmin):
    list_display=("userid","productid","orderdate")
class CartAdmin(admin.ModelAdmin):
    list_display=("product","user","quantity")
admin.site.register(Customers,CustomersAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Products,ProductsAdmin)
# admin.site.register(ProductImages,ProductImagesAdmin)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(Cart,CartAdmin)



