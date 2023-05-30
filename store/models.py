from django.db import models

class Customers(models.Model):
    username=models.CharField(max_length=200,unique=True)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phonenumber=models.IntegerField(max_length=200)
    password=models.CharField(max_length=200)
    repassword=models.CharField(max_length=200)
    isblocked=models.BooleanField(default=False)

class Address(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    country=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    district=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    house=models.CharField(max_length=200)
    pincode=models.PositiveIntegerField()

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    image=models.ImageField(upload_to='store/categorys/', blank=True)
    noofitems=models.IntegerField()
    isblocked=models.BooleanField(default=False)


class Categoryoffer(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    offer_description=models.CharField(max_length=200)
    discount=models.PositiveIntegerField()



     
    
class Products(models.Model):
    name=models.CharField(max_length=200,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    image1=models.ImageField(upload_to='store/products/', blank=True)
    image2=models.ImageField(upload_to='store/products/', blank=True)
    image3=models.ImageField(upload_to='store/products/', blank=True)
    image4=models.ImageField(upload_to='store/products/', blank=True)

class Productoffer(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    offer_description=models.CharField(max_length=200)
    discount=models.PositiveIntegerField()
    




class Cart(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)


class Orders(models.Model):
    user=models.ForeignKey(Customers,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    orderdate=models.DateField(auto_now_add=True)
    orderstatus=models.CharField(max_length=200,default="pending")
    ordertype=models.CharField(max_length=200)
    quantity=models.PositiveIntegerField()
    finalprice=models.DecimalField(max_digits=10, decimal_places=2)
    


class Coupon(models.Model):
    code=models.CharField(max_length=200,unique=True)
    discount_percentage=models.PositiveIntegerField()
    minprice=models.PositiveIntegerField()
    maxprice=models.PositiveIntegerField()
    isavailable=models.BooleanField(default=True)







    