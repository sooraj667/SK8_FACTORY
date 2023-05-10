from django.db import models

class Customers(models.Model):
    username=models.CharField(max_length=200,unique=True)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phonenumber=models.IntegerField(max_length=200)
    password=models.CharField(max_length=200)
    repassword=models.CharField(max_length=200)
    isblocked=models.BooleanField(default=False)

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    noofitems=models.IntegerField()
    


     
    
class Products(models.Model):
    name=models.CharField(max_length=200,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    image1=models.ImageField(upload_to='store/products/', blank=True)
    image2=models.ImageField(upload_to='store/products/', blank=True)
    image3=models.ImageField(upload_to='store/products/', blank=True)
    image4=models.ImageField(upload_to='store/products/', blank=True)

class ProductImages(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products/',blank=True,)
    


class Orders(models.Model):
    userid=models.ForeignKey(Customers,on_delete=models.CASCADE)
    productid=models.ForeignKey(Products,on_delete=models.CASCADE)
    orderdate=models.DateField(auto_now_add=True)
