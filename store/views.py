from django.shortcuts import render,redirect
from .models import *
import re
import random

from twilio.rest import Client
from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from decimal import Decimal
from datetime import date
import paypal
from ecommerce.settings import RAZORPAY_API_SECRET_KEY,RAZORPAY_API_KEY
# Create your views here.

def index(request):
    if "username" in request.session:
        return redirect(loggedin)
    products=Products.objects.all()
    category=Category.objects.all()
    return render(request,"store/index.html",{"products":products,"category":category})

def about(request):
    if "username" in request.session:
        return redirect(loggedin)
    return render(request,"store/about.html")

def blog(request):
    if "username" in request.session:
        return redirect(loggedin)
    return render(request,"store/blog.html")

def contact(request):
    return render(request,"store/contact.html")

def cart(request):
    return render(request,"store/shoping-cart.html")

def shop(request):
    if "username" in request.session:
        return redirect(loggedin)
    products=Products.objects.all()
    # productimages=ProductImages.objects.all()

    return render(request,"store/product.html",{"products":products})



def category_based_product(request,someid):
    categoryobj=Category.objects.get(id=someid)
    productobjs=Products.objects.filter(category=categoryobj)
    return render(request,"store/category_based_product.html",{"productobjs":productobjs})

def loggedincategory_based_product(request,someid):
    categoryobj=Category.objects.get(id=someid)
    productobjs=Products.objects.filter(category=categoryobj)
    return render(request,"store/userdashboard/loggedincategory_based_product.html",{"productobjs":productobjs})

def signup(request): 
    if "username" in request.session:
        return redirect(loggedin)
    if request.method=="POST":
        error={}
        username=request.POST.get("username")
        name=request.POST.get("name")
        email=request.POST.get("email")
        phonenumber=request.POST.get("phonenumber")
        password=request.POST.get("password")
        repassword=request.POST.get("repassword")

        if len(username)<4:
            error["username"]="Username should contain minimum four characters"
        elif len(username)>10:
            error["username"]="Username can only have upto 10 characters"
        elif name.isalpha()=="False":
            error["name"]="Name can't have numbers" 
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            error["email"]="Invalid Email"
        elif phonenumber.isalpha()==True:
            error["phonenumber"]="Phonenumber can't have letters"
        elif len(phonenumber)!=10 or int(phonenumber) < 0:
            error["phonenumber"]="Invalid Phonennumber"
        elif len(password)<6:
            error["password"]="Password must atleast contain 6 characters"
        elif len(password)>12:
            error["password"]="Password can only have upto 12 characters"
        elif password!=repassword:
            error["repassword"]="Passwords doesn't match to Confirm password!"
        else:
            request.session["contactno"]=phonenumber
            fieldvalues=Customers(username=username,name=name,email=email,phonenumber=phonenumber,password=password,repassword=repassword)
            fieldvalues.save()
            messages.success(request, 'Signup successful!')
            return redirect(otplogin)
        
        datas={"error":error,"username":username,"name":name,"email":email,"phonenumber":phonenumber,"password":password,"repassword":repassword,}
        return render(request,"store/signup.html",datas)
            
    return render(request,"store/signup.html")


def otplogin(request):
    if "username" in request.session:
        return redirect(loggedin)
    if request.method=="POST":
        phonenum = '+91' + request.session.get("contactno")
        otp = str(random.randint(100000, 999999))
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        verification = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID) \
                .verifications \
                .create(to=phonenum, channel='sms')
            # Store the phone number and OTP in the session
        request.session['phone_number'] = phonenum
        request.session['otp'] = otp
        request.session['verification_sid'] = verification.sid
        return redirect(verifyotp)
        

    return render(request,"store/otplogin.html")

def verifyotp(request):
    if "username" in request.session:
        return redirect(loggedin)
    msg="Otp sent.Enter the otp recievd in your phone here."
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        phone_number = request.session.get('phone_number')
        phone_number = "+91" + phone_number
        verification_sid = request.session.get('verification_sid')
        # Initialize the Twilio client with your Twilio account SID and auth token
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # Check if the entered OTP is valid
        print("*********")
        print("entered_otp:", entered_otp)
        verification_check = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID) \
            .verification_checks \
            .create(to=phone_number, code=entered_otp, verification_sid=verification_sid)
        if verification_check.status == 'approved':
            request.session["username"]="somevalue"
            return redirect(login)
        else:
            error="Otp doesn't match"
            return render(request,"store/verifyotp.html",{"msg":msg,"error":error})
    return render(request,"store/verifyotp.html",{"msg":msg})

def login(request):
    if "username" in request.session:
        return redirect(loggedin)
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        if len(username)<4:
            error="Username should contain minimum four characters"
        elif len(username)>10:
            error="Username can only have upto 10 characters"
        elif len(password)<6:
            error="Password must altleast contain 6 characters"
        elif len(password)>12:
            error="Password can only have upto 12 characters"
        else:
            try:
                customer = Customers.objects.get(username=username, password=password)
                if not customer.isblocked:
                    request.session["username"] = username
                    return redirect(loggedin)
                else:
                    context = "Account is blocked"
            except Customers.DoesNotExist:
                context = "Invalid Credentials"

            return render(request, "store/login.html", {"context": context})

            
            


        if error:
            return render(request,"store/login.html",{"error":error})
            
    

       

    return render(request,"store/login.html")



def logout(request):
    if "username" in request.session:
        request.session.flush()
    return redirect(login)

def loggedin(request):
    if "username" in request.session:
        category=Category.objects.all()
        products=Products.objects.all()
        cartobjs=Cart.objects.all()
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total
        return render(request,"store/userdashboard/loggedin.html",{"category":category,"products":products,"cartobjs":cartobjs,"totalsum":totalsum})
    else:
        return redirect(login)

def loggedinproduct(request):
    if "username" in request.session:
        products=Products.objects.all()
        cartobjs=Cart.objects.all()
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total

        return render(request,"store/userdashboard/loggedinproduct.html",{"products":products,"cartobjs":cartobjs,"totalsum":totalsum})
    else:
        return redirect(login)

def preview(request,someid):
    if "username" in request.session:
        print(request.session["username"],"######################")
        pdtobj=Products.objects.get(id=someid)
        cartobjs=Cart.objects.all()
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total

        return render(request,"store/userdashboard/preview.html",{"pdtobj":pdtobj,"totalsum":totalsum})
    else:
        return redirect(login)
    
    
def loggedincart(request):
    if "username" in request.session:
        print(request.session["username"],"######################")
        cartobjs=Cart.objects.all()
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total
        return render(request,"store/userdashboard/loggedincart.html",{"cartobjs":cartobjs,"totalsum":totalsum})
    else:
        return redirect(login)
    

def deletecart(request):
    cartobjs=Cart.objects.all()
    cartobjs.delete()
    return JsonResponse({"message":"All items in Cart is deleted!"})

def updatecart(request,someid):
    if request.method=="POST":

        cartobj=Cart.objects.get(id=someid)
        cartobj.quantity=request.POST.get("quantity")
        cartobj.total=cartobj.product.price*Decimal(cartobj.quantity)
        cartobj.save()
        return redirect(loggedincart)




def checkout(request):
    
        
    cartobjs=Cart.objects.all()
    if not cartobjs:
        return redirect(loggedincart)
    totalsum=0
    for item in cartobjs:
        totalsum+=item.total
    client = razorpay.Client(
    auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    amount=int(totalsum*100)
    currency='INR'
    data = dict(amount=amount,currency=currency,payment_capture=1)
            
    payment_order = client.order.create(data=data)
    payment_order_id=payment_order['id']
    print(payment_order)

    if request.method=="POST":
        error={}
        country=request.POST.get("country")
        state=request.POST.get("state")
        district=request.POST.get("district")
        locality=request.POST.get("locality")
        house=request.POST.get("house")
        pincode=request.POST.get("pincode")


        if country.isalpha()=="False":
            error["country"]="Country name can't have numbers"
        elif len(country)<3:
            error["country"]="Country name should contain minimum three characters"
        elif state.isalpha()=="False":
            error["state"]="State name can't have numbers"
        elif len(state)<3:
            error["state"]="State name should contain minimum three characters"
        elif district.isalpha()=="False":
            error["district"]="District name can't have numbers"
        elif len(district)<3:
            error["district"]="District name should contain minimum three characters"
        elif len(locality)<3:
            error["locality"]="Locality name should contain minimum three characters"
        elif len(house)<3:
            error["house"]="House name should contain minimum three characters"
        elif pincode.isalpha()=="True":
            error["pincode"]="Pincode  can't have alphabets"
        elif len(pincode)!=6:
            error["pincode"]="Invalid Pincode"

        else:
            user=request.session["username"]
            userobj=Customers.objects.get(username=user)

            addressvalues=Address(customer=userobj,country=country,state=state,district=district,locality=locality,house=house,pincode=pincode)
            addressvalues.save()
            success='Address Saved successfully!'
            

            
            

                

            return redirect(checkout)
        
        datas={"error":error,"country":country,"state":state,"district":district,"locality":locality,"pincode":pincode}
        return render(request,"store/userdashboard/checkout.html",datas)
    
    cust=Customers.objects.get(username=request.session["username"])
    addressobjs=Address.objects.filter(customer=cust)

    cartobjs=Cart.objects.all()
    totalsum=0
    for item in cartobjs:
        totalsum+=item.total
    return render(request,"store/userdashboard/checkout.html",{"addressobjs":addressobjs,"cartobjs":cartobjs,"totalsum":totalsum,     "amount":300,"order_id":payment_order_id,"api_key":RAZORPAY_API_KEY})

def cashondelivery(request):
    if request.method=="POST":
        action=request.POST.get("action")
        if action=="cashondelivery":


            cartobjs=Cart.objects.all()
            housename=request.POST.get("address")
            print("$$$$$$$$$$$$",housename)
            for item in cartobjs:
                userobj=item.user
                pdtobj=item.product
                quantityobj=item.quantity
                addressobj=Address.objects.get(house=housename)
                orderstatusobj="Ordered"
                ordertypeobj="Cash On Delivery"
                orderdateobj=date.today() 
            orderdata=Orders(user=userobj,product=pdtobj,quantity=quantityobj,address=addressobj,orderstatus=orderstatusobj,orderdate=orderdateobj,ordertype=ordertypeobj)
            orderdata.save()
            cartobjs.delete()
            totalsum=0
            for item in cartobjs:
                totalsum+=item.total

            return render(request,"store/userdashboard/orderplaced.html",{"totalsum":totalsum,"cartobjs":cartobjs})
        
        # elif action=="razorpay":
        #     client = razorpay.Client(
        #     auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        #     amount=2000
        #     currency='INR'
        #     data = dict(amount=amount,currency=currency,payment_capture=1)
                    
        #     payment_order = client.order.create(data=data)
        #     payment_order_id=payment_order['id']
        #     print(payment_order)

        #     cartobjs=Cart.objects.all()
        #     housename=request.POST.get("address")
        #     print("$$$$$$$$$$$$",housename)
        #     for item in cartobjs:
        #         userobj=item.user
        #         pdtobj=item.product
        #         quantityobj=item.quantity
        #         addressobj=Address.objects.get(house=housename)
        #         orderstatusobj="Ordered"
        #         ordertypeobj="Cash On Delivery"
        #         orderdateobj=date.today() 
        #     orderdata=Orders(user=userobj,product=pdtobj,quantity=quantityobj,address=addressobj,orderstatus=orderstatusobj,orderdate=orderdateobj,ordertype=ordertypeobj)
        #     orderdata.save()
        #     cartobjs.delete()
        #     totalsum=0
        #     for item in cartobjs:
        #         totalsum+=item.total

        #     return render(request,"store/userdashboard/checkout.html",{ "amount":200,"order_id":payment_order_id,"api_key":RAZORPAY_API_KEY})
    return HttpResponse("Invalid request")


def addtocart(request,someid):
   

        if request.method=="POST":

            pdtobj=Products.objects.get(id=someid)

            print(pdtobj.name,"################")

            currentuser=request.session["username"]

            print(currentuser,"########################")
            userobj=Customers.objects.get(username=currentuser)
            quantity=request.POST.get("quantity")
            total=Decimal(quantity)*pdtobj.price
            # if quantity is None:
            #     quantity=1

            cartadd=Cart(product=pdtobj,user=userobj,quantity=int(quantity),total=total)
            cartadd.save()
            return redirect(loggedincart) 

def previousorders(request):
    orderobjs=Orders.objects.all()
    return render(request,"store/userdashboard/previousorders.html",{"orderobjs":orderobjs})

# def buynow(request,someid):
#     if "username" in request.session:
#         if request.method=="POST":
#             # authorize razorpay client with API Keys.
#             client = razorpay.Client(
#             auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
#             amount=200
#             currency='INR'
#             data = dict(amount=amount,currency=currency,payment_capture=1)
            
#             payment_response = client.order.create(data=data)
#             print(payment_response)


#             usname=request.session["username"] #This session is created during login
#             user=Customers.objects.get(username=usname)
#             product=Products.objects.get(id=someid)
#             ord=Orders(productid=product,userid=user)
#             ord.save()
#             return render(request,"store/orderconfirmed.html",{"pdt":product,"user":user})


#         product=Products.objects.get(id=someid)
#         return render(request,"store/buynow.html",{"product":product})


def cancelorder(request,someid):

    print(someid,"SOMEID ***********")
    orderobj=Orders.objects.get(id=someid)
    orderobj.orderstatus="Cancelled"
    orderobj.save()

    print("******************")
    print(orderobj.orderstatus)
    print("******************")


    return JsonResponse({"message": "Confirm !"})