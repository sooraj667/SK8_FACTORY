from django.shortcuts import render,redirect
from .models import *
import re
import random
from django.conf import settings
from twilio.rest import Client
from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from decimal import Decimal
# Create your views here.

def index(request):
    if "username" in request.session:
        return redirect(loggedin)
    return render(request,"store/index.html")

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
        elif len(phonenumber)!=10:
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

            
            
            # fieldvalues=Customers.objects.get(username=username,password=password)
            # count=Customers.objects.get(username=username,password=password).count()
            # if count==1 and fieldvalues.isblocked==False:
            #     # request.session["username"]=username
            #     return redirect(otplogin)
            # if count!=1 or fieldvalues.isblocked==True:
            #     context="Invalid Credentials"
            #     return render(request,"store/login.html",{"context":context}) 


        if error:
            return render(request,"store/login.html",{"error":error})
            
    

       

    return render(request,"store/login.html")



def logout(request):
    if "username" in request.session:
        request.session.flush()
    return redirect(login)

def loggedin(request):
    if "username" in request.session:
        return render(request,"store/userdashboard/loggedin.html")
    else:
        return redirect(login)

def loggedinproduct(request):
    if "username" in request.session:
        products=Products.objects.all()
        return render(request,"store/userdashboard/loggedinproduct.html",{"products":products})
    else:
        return redirect(login)

def preview(request,someid):
    if "username" in request.session:
        print(request.session["username"],"######################")
        pdtobj=Products.objects.get(id=someid)
        return render(request,"store/userdashboard/preview.html",{"pdtobj":pdtobj})
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
            return redirect(loggedinproduct) 



def buynow(request,someid):
    if "username" in request.session:
        if request.method=="POST":
            # authorize razorpay client with API Keys.
            razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
            amount=200
            order_currency='INR'
            data = {
            'amount': int(amount),
            'currency': 'INR',
            'payment_capture': 1
            }
            # order = client.order.create(data=data)


            usname=request.session["username"] #This session is created during login
            user=Customers.objects.get(username=usname)
            product=Products.objects.get(id=someid)
            ord=Orders(productid=product,userid=user)
            ord.save()
            return render(request,"store/orderconfirmed.html",{"pdt":product,"user":user})


        product=Products.objects.get(id=someid)
        return render(request,"store/buynow.html",{"product":product})

