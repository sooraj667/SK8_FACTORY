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
from decimal import Decimal

import requests




def index(request):
    if "username" in request.session:
        return redirect(loggedin)
    products=Products.objects.all()
    category=Category.objects.all()
    
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
        
    return render(request,"store/index.html",{"products":products,"category":category,"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount})

def about(request):
    if "username" in request.session:
        return redirect(loggedin)
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
    context={"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount}
    return render(request,"store/about.html",context)

def guestcontact(request):
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
    context={"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount}
    return render(request,"store/guestcontact.html",context)

def blog(request):
    if "username" in request.session:
        return redirect(loggedin)
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
    context={"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount}
    return render(request,"store/blog.html",context)

def contact(request):
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0   
    context={"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount}
    return render(request,"store/contact.html",context)

# def cart(request):
#     if "cartdict" in request.session:
#         cartdict=request.session["cartdict"]
#         subtotal=0
#         for k,v in cartdict.items():
#             subtotal+=v["total"]
#     context={"cartdict":cartdict,"totalsum":subtotal}
    # return render(request,"store/shoping-cart.html",context)

def shop(request):
    if "username" in request.session:
        return redirect(loggedin)
    products=Products.objects.all()
    filterpricedict={"1":"Below Rs.1000","2":"Rs.1000.00 - Rs.4000.00","3":"Rs.4000.00 - Rs.10000.00","4":"Above Rs.10000"}
    categoryobjs=Category.objects.all()
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  

    context={"filterpricedict":filterpricedict,"categoryobjs":categoryobjs,"products":products,"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount}
    return render(request,"store/product.html",context)

def guestfilterprice(request,someid):
    if "username" in request.session:
        return redirect(loggedin)
    priceid=someid

    if priceid==1:
        products=Products.objects.filter(price__lte=1000)
    elif priceid==2:
        products=Products.objects.filter(price__range=(1000,4000))
    elif priceid==3:
        products=Products.objects.filter(price__range=(4000,10000))
    else:
        products=Products.objects.filter(price__gte=10000)

    filterpricedict={"1":"Below Rs.1000","2":"Rs.1000.00 - Rs.4000.00","3":"Rs.4000.00 - Rs.10000.00","4":"Above Rs.10000"}
    categoryobjs=Category.objects.all()
    context={"filterpricedict":filterpricedict,"categoryobjs":categoryobjs,"products":products}
    return render(request,"store/product.html",context)

def guestfiltercategory(request,someid):
    if "username" in request.session:
        return redirect(loggedin)
    category=Category.objects.get(id=someid)
    products=Products.objects.filter(category=category)
    filterpricedict={"1":"Below Rs.1000","2":"Rs.1000.00 - Rs.4000.00","3":"Rs.4000.00 - Rs.10000.00","4":"Above Rs.10000"}
    categoryobjs=Category.objects.all()
    context={"filterpricedict":filterpricedict,"categoryobjs":categoryobjs,"products":products}
    return render(request,"store/product.html",context)



def guestpreview(request,someid):
       
    
        pdtobj=Products.objects.get(id=someid)
        if request.method=="POST":
            
                

                

            if "addtocart" in request.POST:

             
                pdtobj=Products.objects.get(id=someid)
                pdtname=pdtobj.name                
                quantity=int(request.POST.get("quantity"))
                totalprice=pdtobj.price*Decimal(quantity)
                totalprice=float(totalprice)
                print(totalprice,"llllllllllllllllllll")
              
                

                # if ("product"+str(pdtobj.id)) in request.session:
                    # request.session["product"+str(pdtobj.id)]=pdtname
                    # request.session["quantity"+str(pdtobj.id)]+=quantity
                    # request.session["totalprice"+str(pdtobj.id)]+=totalprice
                
                
                # else:

                    # request.session["product"+str(pdtobj.id)]=pdtname
                    # request.session["quantity"+str(pdtobj.id)]=quantity
                    # request.session["totalprice"+str(pdtobj.id)]=totalprice
                    # if not "cartcount" in request.session:
                    #     request.session["cartcount"]=[str(pdtobj.id)]
                    # else:
                    #     request.session["cartcount"].append(str(pdtobj.id))

                



                if "cartdict" not in request.session:
                    request.session["cartdict"]={}          
                    request.session["cartdict"][str(pdtobj.id)]={}
                    cartdict=request.session["cartdict"]
                    cartdict[str(pdtobj.id)]["product"]=pdtname
                    cartdict[str(pdtobj.id)]["quantity"]=quantity
                    cartdict[str(pdtobj.id)]["total"]=totalprice
                    cartdict[str(pdtobj.id)]["image"]=pdtobj.image1.url
                    request.session["cartdict"]=cartdict

                if str(pdtobj.id) not in request.session["cartdict"].keys():
                    request.session["cartdict"][str(pdtobj.id)]={}
                    cartdict=request.session["cartdict"]
                    cartdict[str(pdtobj.id)]["product"]=pdtname
                    cartdict[str(pdtobj.id)]["quantity"]=quantity
                    cartdict[str(pdtobj.id)]["total"]=totalprice
                    cartdict[str(pdtobj.id)]["image"]=pdtobj.image1.url
                    request.session["cartdict"]=cartdict

                else:
                    cartdict=request.session["cartdict"]
                    cartdict[str(pdtobj.id)]["product"]=pdtname
                    cartdict[str(pdtobj.id)]["quantity"]+=quantity
                    cartdict[str(pdtobj.id)]["total"]+=totalprice
                    cartdict[str(pdtobj.id)]["image"]=pdtobj.image1.url
                    request.session["cartdict"]=cartdict

                return redirect(guestcart)


                

                


        

               
            
        if "cartdict" in request.session:
            cartdict=request.session["cartdict"]
            subtotal=0
            for k,v in cartdict.items():
                subtotal+=v["total"]
            cartcount=len(cartdict)
        else:
            cartdict={}
            subtotal=0
            cartcount=0
        if "wishlistdict" in request.session:
            wishlistdict=request.session["wishlistdict"]
            wishcount=len(wishlistdict) 
        else:
            wishcount=0  
            wishlistdict={}
         

       
   
        return render(request,"store/guestpreview.html",{"pdtobj":pdtobj,"wishcount":wishcount,"cartcount":cartcount,"cartdict":cartdict,"totalsum":subtotal})


def guestcart(request):
    # if "cartcount" not in request.session:
    #     return render(request,"store/guestcart.html",{"message":"Cart is empty"} )

    if "cartdict" not in request.session:
        return render(request,"store/guestcart.html",{"message":"Cart is empty"} )
    
    cartdict=request.session["cartdict"]
    subtotal=float(0)
    for key,value in cartdict.items():
        subtotal+=value["total"]
    request.session["subtotal"]=subtotal
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
    context={"cartdict":cartdict,"subtotal":subtotal,"wishcount":wishcount,"cartcount":cartcount}
    return render(request,"store/guestcart.html",context)
    







    # cartlist=request.session.get("cartcount")
    # if "cartdict" not in request.session:
    #     cartdict={}
    # else:
    #     cartdict=request.session["cartdict"]
    # for item in cartlist:
    #     product=request.session["product"+item]
    #     quantity=request.session["quantity"+item]
    #     total=request.session["totalprice"+item]
    #     productobj=Products.objects.get(name=product)
    #     pdtimage=productobj.image1
    #     print("MYRRR",pdtimage)
    #     if item not in cartdict:
    #         cartdict[item]={}
    #         cartdict[item]["product"]=product
    #         cartdict[item]["quantity"]=quantity
    #         cartdict[item]["total"]=total
    #         cartdict[item]["image"]=pdtimage.url
    #     else:
    #         cartdict[item]["product"]=product
    #         cartdict[item]["quantity"]+=quantity
    #         cartdict[item]["total"]+=total
    #         cartdict[item]["image"]=pdtimage.url
    #     request.session["cartdict"]=cartdict

    # subtotal=0
    # for k,v in cartdict.items():
    #     subtotal+=v["total"]
    # request.session["subtotal"]=subtotal
    # print("BROOOOOOOOO",cartdict)
    # context={"cartdict":cartdict,"subtotal":subtotal}
    # return render(request,"store/guestcart.html",context)



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

        already_presentuser=None
        try:
            already_presentuser=Customers.objects.get(username=username)
        except:
            pass
      

        if len(username)<4:
            error["username"]="Username should contain minimum four characters"
        elif len(username)>10:
            error["username"]="Username can only have upto 10 characters"
        elif already_presentuser:
            error["username"]="Username already taken.Please choose any other"
        elif name.isalpha()=="False":
            error["name"]="Name can't have numbers" 
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            error["email"]="Invalid Email"
        elif Customers.objects.filter(email=email):
            error["email"]="Email already exists! Please Use a different email"
        elif phonenumber.isalpha()==True:
            error["phonenumber"]="Phonenumber can't have letters"
        elif not re.match(r"^\d{10}$",phonenumber):
            error["phonenumber"]="Invalid Phone number"
        elif len(phonenumber)!=10:
            error["phonenumber"]="Invalid Phonennumber"
        elif phonenumber[0]==0:
            error["phonenumber"]="Invalid Phone number"
        elif int(phonenumber)<0:
            error["phonenumber"]="Phone number can't be negative value"  
        elif Customers.objects.filter(phonenumber=phonenumber):
            error["phonenumber"]="Phone number already exists! Please Use a differnet number"
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
            request.session["guestuser"]="guestuser"
            
            return redirect(otplogin)
        
        datas={"error":error,"username":username,"name":name,"email":email,"phonenumber":phonenumber,"password":password,"repassword":repassword,}
        return render(request,"store/signup.html",datas)
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
    context={"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount}     
    return render(request,"store/signup.html",context)




def generate_otp():
    return str(random.randint(1000, 9999))

# request.session.get("contactno")
def otplogin(request):
    if "username" in request.session:
        return redirect(loggedin)
    if request.method=="POST":
        phonenumber=request.POST["phonenumber"]
        cust=Customers.objects.filter(phonenumber=phonenumber).count()
        if cust==0:
            error="Phonenumber not registered"
            return render(request,"store/otplogin.html",{"error":error})
        else:
            
            otp = generate_otp()
            
            request.session['U_otp'] = otp
            request.session['U_phone'] = phonenumber
            
            send_otp(phonenumber, otp)
            
            return redirect(verifyotp)
    
        

    return render(request,"store/otplogin.html")


def send_otp(phonenumber, otp):
    url = 'https://www.fast2sms.com/dev/bulkV2'
    payload = f'sender_id=TXTIND&message={otp}&route=v3&language=english&numbers={phonenumber}'
    headers = {
        'authorization': "9mCRNewf4y51lc6KJLFYIgZtEjxv0WV3PuoHOra2BphzsGUMiqwmdFs3TZfEMB2vkcG5JqNeRSyCj8Yp",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def verifyotp(request):
    if "username" in request.session:
        return redirect(loggedin)
    msg="Otp sent.Please enter the otp recieved in your phone."
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        if 'U_otp' in request.session and 'U_phone' in request.session:
            exact_otp = request.session['U_otp']
            phonenumber = request.session['U_phone']
            if exact_otp == user_otp:
                try:
                    
                    user = Customers.objects.get(phonenumber=phonenumber)
                    
                    if user is not None:

                        request.session['username'] = user.username 
                        request.session['phonenumber'] = phonenumber
                        # messages.success(request, "Login completed successfully")
                        return redirect(loggedin)
                except Customers.DoesNotExist:
                    messages.error(request, "This User doesn't Exist")
            else:
                # messages.error(request, "Invalid OTP. Please try again.")
                error="Otp doesn't match"
                return render(request,"store/verifyotp.html",{"msg":msg,"error":error})
    return render(request,"store/verifyotp.html",{"msg":msg})





    #     phone_number = request.session.get('phone_number')
    #     phone_number = "+91" + phone_number
    #     verification_sid = request.session.get('verification_sid')
    #     # Initialize the Twilio client with your Twilio account SID and auth token
    #     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #     # Check if the entered OTP is valid
    #     print("*********")
    #     print("entered_otp:", entered_otp)
    #     verification_check = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID) \
    #         .verification_checks \
    #         .create(to=phone_number, code=entered_otp, verification_sid=verification_sid)
    #     if verification_check.status == 'approved':
    #         request.session["username"]="somevalue"
    #         return redirect(login)
    #     else:
    #         error="Otp doesn't match"
    #         return render(request,"store/verifyotp.html",{"msg":msg,"error":error})
    # return render(request,"store/verifyotp.html",{"msg":msg})

def login(request):
    try:
        if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
            return redirect(loggedin)
    except:
        pass
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
                
        
    
    
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
    context={"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount} 
    return render(request,"store/login.html",context)



def logout(request):
    if "username" in request.session:
        request.session.flush()
    return redirect(login)



def filtercategory(request,someid):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        category=Category.objects.get(id=someid)
        products=Products.objects.filter(category=category)
        
        extracheapproducts = Products.objects.filter(price__lte=1000)
        cheapproducts = Products.objects.filter(price__range=(1000,4000))
        mediumproducts = Products.objects.filter(price__range=(4000,10000))
        expensiveproducts = Products.objects.filter(price__gte=10000)


        categoryobjs=Category.objects.all()
        

        



        filterpricedict={"1":"Below Rs.1000","2":"Rs.1000.00 - Rs.4000.00","3":"Rs.4000.00 - Rs.10000.00","4":"Above Rs.10000"}
        userobj=Customers.objects.get(username=request.session["username"])
        cartobjsfiltered=Cart.objects.filter(user=userobj)
        cartobjs=Cart.objects.filter(user=userobj)
        no_of_cart_items=cartobjsfiltered.count()
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total
        context={"products":products,"cartobjs":cartobjs,"totalsum":totalsum,"no_of_cart_items":no_of_cart_items,"extracheapproducts":extracheapproducts,"cheapproducts":cheapproducts,"mediumproducts":mediumproducts,"expensiveproducts":expensiveproducts,"categoryobjs":categoryobjs,"filterpricedict":filterpricedict}
        return render(request,"store/userdashboard/loggedinproduct.html",context)
    else:
        return redirect(login)
    
def filterprice(request,someid):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        priceid=someid

        if priceid==1:
            products=Products.objects.filter(price__lte=1000)
        elif priceid==2:
            products=Products.objects.filter(price__range=(1000,4000))
        elif priceid==3:
            products=Products.objects.filter(price__range=(4000,10000))
        else:
            products=Products.objects.filter(price__gte=10000)



        
        extracheapproducts = Products.objects.filter(price__lte=1000)
        cheapproducts = Products.objects.filter(price__range=(1000,4000))
        mediumproducts = Products.objects.filter(price__range=(4000,10000))
        expensiveproducts = Products.objects.filter(price__gte=10000)


        categoryobjs=Category.objects.all()
        

        



        filterpricedict={"1":"Below Rs.1000","2":"Rs.1000.00 - Rs.4000.00","3":"Rs.4000.00 - Rs.10000.00","4":"Above Rs.10000"}
        userobj=Customers.objects.get(username=request.session["username"])
        cartobjsfiltered=Cart.objects.filter(user=userobj)
        cartobjs=Cart.objects.filter(user=userobj)
        no_of_cart_items=cartobjsfiltered.count()
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total
        context={"products":products,"cartobjs":cartobjs,"totalsum":totalsum,"no_of_cart_items":no_of_cart_items,"extracheapproducts":extracheapproducts,"cheapproducts":cheapproducts,"mediumproducts":mediumproducts,"expensiveproducts":expensiveproducts,"categoryobjs":categoryobjs,"filterpricedict":filterpricedict}
        return render(request,"store/userdashboard/loggedinproduct.html",context)
    else:
        return redirect(login)









def loggedin(request):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        if "cartdict" in request.session and "guestuser" in request.session:
            cartdict=request.session["cartdict"]
            for item,data in cartdict.items():
                user=Customers.objects.get(username=request.session["username"])
                product=Products.objects.get(id=int(item))
                quantity=data["quantity"]
                total=data["total"]
                cartobj=Cart(user=user,product=product,quantity=quantity,total=total)
                cartobj.save()
            del request.session["cartdict"]
            del request.session["guestuser"]



        category=Category.objects.all()
        products=Products.objects.all()

        categoryofferobjs=Categoryoffer.objects.all()
        userobj=Customers.objects.get(username=request.session["username"])

        cartobjs=Cart.objects.filter(user=userobj)
        wishlistobjs=Wishlist.objects.filter(user=userobj)
        no_of_wishlist_items=wishlistobjs.count()
        no_of_cart_items=cartobjs.count()
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total
        return render(request,"store/userdashboard/loggedin.html",{"category":category,"products":products,"cartobjs":cartobjs,"totalsum":totalsum,       "categoryofferobjs":categoryofferobjs,"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items})
    else:
        return redirect(login)
    
def loggedincontact(request):
    userobj=Customers.objects.get(username=request.session["username"])
    cartobjs=Cart.objects.filter(user=userobj)
    subtotal=0
    for item in cartobjs:
        subtotal+=item.total

    no_of_cart_items=cartobjs.count()
    wishlistobjs=Wishlist.objects.filter(user=userobj)
    no_of_wishlist_items=wishlistobjs.count()
    context={"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items,"cartobjs":cartobjs,"totalsum":subtotal}
    return render(request,"store/userdashboard/loggedincontact.html",context)

def loggedinabout(request):
    userobj=Customers.objects.get(username=request.session["username"])
    cartobjs=Cart.objects.filter(user=userobj)
    no_of_cart_items=cartobjs.count()
    
    wishlistobjs=Wishlist.objects.filter(user=userobj)
    no_of_wishlist_items=wishlistobjs.count()
    subtotal=0
    for item in cartobjs:
        subtotal+=item.total
    context={"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items,"cartobjs":cartobjs,"totalsum":subtotal}
    return render(request,"store/userdashboard/loggedinabout.html",context)

def loggedinproduct(request):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        products=Products.objects.all()
        
        extracheapproducts = Products.objects.filter(price__lte=1000)
        cheapproducts = Products.objects.filter(price__range=(1000,4000))
        mediumproducts = Products.objects.filter(price__range=(4000,10000))
        expensiveproducts = Products.objects.filter(price__gte=10000)
        filterpricedict={"1":"Below Rs.1000","2":"Rs.1000.00 - Rs.4000.00","3":"Rs.4000.00 - Rs.10000.00","4":"Above Rs.10000"}

        categoryobjs=Category.objects.all()
        

        



        userobj=Customers.objects.get(username=request.session["username"])
        cartobjsfiltered=Cart.objects.filter(user=userobj)
        cartobjs=Cart.objects.filter(user=userobj)
        no_of_cart_items=cartobjsfiltered.count()
        
        wishlistobjs=Wishlist.objects.filter(user=userobj)
        no_of_wishlist_items=wishlistobjs.count()

        totalsum=0
        for item in cartobjs:
            totalsum+=item.total
        context={"products":products,"cartobjs":cartobjs,"totalsum":totalsum,"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items ,"extracheapproducts":extracheapproducts,"cheapproducts":cheapproducts,"mediumproducts":mediumproducts,"expensiveproducts":expensiveproducts,"categoryobjs":categoryobjs,"filterpricedict":filterpricedict}
        return render(request,"store/userdashboard/loggedinproduct.html",context)
    else:
        return redirect(login)

def preview(request,someid):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        pdtobj=Products.objects.get(id=someid)
        username=request.session["username"]
        user=Customers.objects.get(username=username)

        categoryofferobjs=Categoryoffer.objects.all()
        productofferobjs=Productoffer.objects.all()

        categoryfound=False
        productfound=False
        for cat in categoryofferobjs:
            if cat.category==pdtobj.category:
                categoryfound=True
                break
        for pdt in productofferobjs:
            if pdt.product ==pdtobj:
                productfound=True
                break



        user=Customers.objects.get(username=request.session.get("username"))
        cartobjs=Cart.objects.filter(user=user)
        no_of_cart_items=cartobjs.count()


        totalsum=0
        for item in cartobjs:
            totalsum+=item.total

        offers=Productoffer.objects.filter(product=pdtobj)
        price_after_discount=pdtobj.price
        if request.method=="POST":
            if "addoffer" in request.POST:

                
                catoffer=None
                pdtoffer=None
                try:
                    catoffer=request.POST["catofferselect"]
                except:
                    pass
                try:
                    pdtoffer=request.POST["pdtofferselect"]
                except:
                    pass
                if catoffer:
                    catofferobj=Categoryoffer.objects.get(category=pdtobj.category,offer_description=catoffer)
                    category_discount=catofferobj.discount
                if pdtoffer:
                    pdtofferobj=Productoffer.objects.get(product=pdtobj,offer_description=pdtoffer)
                    product_discount=pdtofferobj.discount
                    
                if catoffer and pdtoffer:

                    if category_discount>=product_discount:
                        discount=category_discount
                        offer=catoffer
                    else:
                        discount=product_discount
                        offer=pdtoffer
                if catoffer and not pdtoffer:
                    discount=category_discount
                    offer=catoffer
                if not catoffer and pdtoffer:
                    discount=product_discount
                    offer=pdtoffer
                try:
                    price_after_discount=pdtobj.price-(Decimal(discount/100)*pdtobj.price)
                    price_after_discount=float(price_after_discount)
                    print(price_after_discount,"ADDOFFERRRR")
                    return render(request,"store/userdashboard/preview.html",{"pdtobj":pdtobj,"totalsum":totalsum,"price_after_discount":price_after_discount,"offer":offer,     "offers":offers,"categoryfound":categoryfound,"productfound":productfound,"categoryofferobjs":categoryofferobjs,"no_of_cart_items":no_of_cart_items})
                except:
                    pass
                

                

            if "addtocart" in request.POST:

                final_product_prize=request.POST.get("price_after_discount")
                pdtobj=Products.objects.get(id=someid)
                

             

            

                currentuser=request.session["username"]

                
                userobj=Customers.objects.get(username=currentuser)
                cartobjs=Cart.objects.filter(user=userobj)
                quantity=request.POST.get("quantity")
                offer=request.POST.get("pdtoffer")
                
              
                    
                total=Decimal(quantity)*Decimal(final_product_prize)
                print("$$$$$$$$$$$$$$$",total)
                cartdict={}
                if cartobjs:
                    
                    for item in cartobjs:
                        if item.product.name not in cartdict:
                            cartdict[item.product.name]=item.quantity
                        else:
                            cartdict[item.product.name]+=item.quantity
                    try:

                        if cartdict[pdtobj.name]:

                            remaining_quantity=pdtobj.quantity-cartdict[pdtobj.name]
                        if not cartdict[pdtobj.name]:
                            remaining_quantity=pdtobj.quantity

                        print("***********",quantity,remaining_quantity)

                        if int(quantity)>remaining_quantity:
                            error="Product Out of Stock"
                            # return render(request,"store/userdashboard/preview.html",{"error":error})
                            return redirect(preview,someid)
                    except:
                        pass

                for cartitem in cartobjs:
                    if cartitem.product==pdtobj:
                        cartitem.quantity+= int(quantity)
                        cartitem.save()
                        return redirect(loggedincart)

                


        

                cartadd=Cart(product=pdtobj,user=userobj,quantity=int(quantity),total=total)
                cartadd.save()
                return redirect(loggedincart)


        wishlistobjs=Wishlist.objects.filter(user=user)
        

        cartobjs=Cart.objects.filter(user=user)
        no_of_cart_items=cartobjs.count()
        
        no_of_wishlist_items=wishlistobjs.count()



        totalsum=0
        for item in cartobjs:
            totalsum+=item.total

        

        return render(request,"store/userdashboard/preview.html",{"pdtobj":pdtobj,"totalsum":totalsum,     "offers":offers,"categoryofferobjs":categoryofferobjs,"categoryfound":categoryfound,"productfound":productfound,"no_of_cart_items":no_of_cart_items  ,"no_of_wishlist_items":no_of_wishlist_items,"cartobjs":cartobjs,"totalsum":totalsum,})
    else:
        return redirect(login)
    
    
def loggedincart(request):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        userobj=Customers.objects.get(username=request.session["username"])
        cartobjs=Cart.objects.filter(user=userobj)
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total

        no_of_cart_items=cartobjs.count()
        wishlistobjs=Wishlist.objects.filter(user=userobj)
        no_of_wishlist_items=wishlistobjs.count()
        return render(request,"store/userdashboard/loggedincart.html",{"cartobjs":cartobjs,"totalsum":totalsum,"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items})
    else:
        return redirect(login)
    

def deletecart(request):
    cartobjs=Cart.objects.all()
    cartobjs.delete()
    return JsonResponse({"message":"All items in Cart is deleted!"})

def updatecart(request,someid):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        if request.method=="POST":

            cartobj=Cart.objects.get(id=someid)
            print(cartobj.id,"BRO")
            cartobj.quantity=request.POST.get("quantity")
            cartobj.total=cartobj.product.price*Decimal(cartobj.quantity)
            cartobj.save()
            return redirect(loggedincart)

def quantityupdate(request):
    itemid=request.GET["itemid"]
    quantity=request.GET["quantity"]
    cartobj=Cart.objects.get(id=itemid)
    product=cartobj.product
    cartobj.quantity=quantity
    sum=Decimal(quantity)*product.price
    cartobj.total=sum
    
    cartobj.save()
    username=request.session["username"]
    userobj=Customers.objects.get(username=username)
    cartobjs=Cart.objects.filter(user=userobj)
    subtotal=0
    for item in cartobjs:
        subtotal+=item.total
    
    print("ENTE ALIYA *******************************")
    return JsonResponse({"sum":sum,"subtotal":subtotal})

def guestquantityupdate(request):
    itemid=request.GET["itemid"]
    quantity=int(request.GET["quantity"])
   
    product=Products.objects.get(id=int(itemid))
    sum=Decimal(quantity)*product.price
    
    cartdict=request.session["cartdict"]

    

    cartdict[str(itemid)]["quantity"]=quantity
    cartdict[str(itemid)]["total"]=float(sum)

    
    request.session["cartdict"]=cartdict
    


    

    cartdict=request.session["cartdict"]
    subtotal=0
    for k,v in cartdict.items():
        subtotal+=v["total"]
    
    
    request.session["subtotal"]=float(subtotal)
    
 



    return JsonResponse({"sum":sum,"subtotal":subtotal})


def guestdeletecartitem(request):
    cartid=request.GET["cartid"]
    # subtotal=float(request.GET["subtotal"])
    # cartdict=request.session["cartdict"]
    # amount=cartdict[str(cartid)]["total"]
    
    # cartlist=request.session.get("cartcount")
    # if str(cartid) in cartlist:
    #     cartlist.remove(str(cartid))
    
    # strcartid=str(cartid)
    # del request.session["cartdict"][strcartid]
    # request.session["cartcount"].remove(strcartid)
    # print(request.session["cartdict"],"FLINGO")
    # del request.session["quantity"+strcartid]
    # del request.session["product"+strcartid]
    # # del request.session[strcartid]
    
    # del request.session["totalprice"+strcartid]

    
    # print("VASUU",cartdict)
    # subtotal=request.session["subtotal"]
    # totalsum=float(subtotal)-float(amount)



    cartdict=request.session["cartdict"]
    amount=cartdict[str(cartid)]["total"]
    request.session["subtotal"]-=amount
    totalsum=request.session["subtotal"]
    del cartdict[str(cartid)]
    request.session["cartdict"]=cartdict

    
    return JsonResponse({"message":"removed","totalsum":totalsum})





def deletecartitem(request):
    cartid=request.GET["cartid"]
    subtotal=float(request.GET["subtotal"])
    cartobj=Cart.objects.get(id=cartid)
    amount=cartobj.total
    totalsum=Decimal(subtotal)-amount

    cartobj.delete()

    return JsonResponse({"message":"removed","totalsum":totalsum})



def increasequantity(request,itemid):
    cartobj=Cart.objects.get(id=itemid)
    updatedquantity = request.GET.get('updatedquantity')
    print("MWONEE",updatedquantity)
    cartobj.quantity=updatedquantity

    return JsonResponse({"message":"Updated"})

# totalsum_withcoupon=request.GET.get("totalsum_withcoupon")

def checkout(request):
    if Customers.objects.get(username=request.session["username"]).isblocked:
        return redirect(login)
    
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked: 
        userobj=Customers.objects.get(username=request.session["username"])   
        cartobjs=Cart.objects.filter(user=userobj)
        if not cartobjs:
            return redirect(loggedin)
            
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
        totalsum_withcoupon=None

        if request.method=="POST":
            if "addressform" in request.POST:
                
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
                
                datas={"error":error,"country":country,"state":state,"district":district,"locality":locality,"pincode":pincode,"house":house}
                return render(request,"store/userdashboard/checkout.html",datas)
        cust=Customers.objects.get(username=request.session["username"])
        addressobjs=Address.objects.filter(customer=cust)

        cartobjs=Cart.objects.filter(user=cust)
        totalsum=0
        for item in cartobjs:
            totalsum+=item.total


        if totalsum_withcoupon:
            totalsum=totalsum_withcoupon
        couponobjs=Coupon.objects.all()

        cartobjsfiltered=Cart.objects.filter(user=cust)
        no_of_cart_items=cartobjsfiltered.count()
        return render(request,"store/userdashboard/checkout.html",{"addressobjs":addressobjs,"cartobjs":cartobjs,"totalsum":totalsum,"couponobjs":couponobjs,"no_of_cart_items":no_of_cart_items,     "amount":300,"order_id":payment_order_id,"api_key":RAZORPAY_API_KEY})


# def applycoupon(request):
#     if request.method=="POST":
#         coup=request.POST["coupon_select"]
#         couponobj=Coupon.objects.get(code=coup)
#         cartobjs=Cart.objects.all()

#         discount_percentage=couponobj.discount_percentage
#         totalsum=0
#         for item in cartobjs:
#             totalsum+=item.total

#         totalsum_withcoupon=float(totalsum)-((discount_percentage/100)*(totalsum))
#         return redirect (checkout,totalsum_withcoupon=totalsum_withcoupon) 

  
def applycouponajax(request):
    print("#############VIEW REACHED")
    couponid=request.GET["couponid"]
    total=float(request.GET["totalamount"])
    couponobj=Coupon.objects.get(code=couponid)
    if total<couponobj.minprice:
        reqamount=couponobj.minprice-total
        discounted_amount=total
        message=f"Sorry add {reqamount} to apply for this coupon"
        return JsonResponse({"amount":discounted_amount,"message":message})
        
    else:
        discounted_amount=total-((couponobj.discount_percentage/100)*total)

        message_success=f"{couponid} - Coupon applied"
        return JsonResponse({"amount":discounted_amount,"message_success":message_success})




    



def cashondelivery(request):
    if request.method=="POST":
        action = request.POST.get("action")
        if action == "cashondelivery":
        

            username=request.session["username"]
            user=Customers.objects.get(username=username)
            cartobjs=Cart.objects.filter(user=user)
            housename=request.POST.get("address")
            print("$$$$$$$$$$$$",housename)
            for item in cartobjs:
                userobj=item.user
                pdtobj=item.product
                quantityobj=item.quantity
                try:
                    addressobj=Address.objects.get(house=housename)
                except:
                    messages.error(request, "Address cannot be empty.")
                    return redirect(checkout)
                orderstatusobj="Ordered"
                if "cashondeliverybutton" in request.POST:
                    ordertypeobj="Cash On Delivery"
                elif "razorpaybutton" in request.POST:
                    ordertypeobj="Razor Pay"
                orderdateobj=date.today() 
                finalprice=item.total
                orderdata=Orders(user=userobj,product=pdtobj,quantity=quantityobj,address=addressobj,orderstatus=orderstatusobj,orderdate=orderdateobj,ordertype=ordertypeobj,finalprice=finalprice)
                orderdata.save()

                pdtobj.quantity=pdtobj.quantity-item.quantity
                pdtobj.save()
            cartobjs.delete()
            totalsum=0
            for item in cartobjs:
                totalsum+=item.total
            

            no_of_cart_items=cartobjs.count()

            

            return render(request,"store/userdashboard/orderplaced.html",{"totalsum":totalsum,"cartobjs":cartobjs,"no_of_cart_items":no_of_cart_items})
        
        #  elif "razorpay" in request.POST:
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


# def addtocart(request,someid):
   

#         if request.method=="POST":

#             pdtobj=Products.objects.get(id=someid)
#             cartobjs=Cart.objects.all()

            

           

#             currentuser=request.session["username"]

            
#             userobj=Customers.objects.get(username=currentuser)
#             quantity=request.POST.get("quantity")
#             offer=request.POST.get("offer")
#             total=Decimal(quantity)*pdtobj.price
#             cartdict={}
#             if cartobjs:
                
#                 for item in cartobjs:
#                     if item.product.name not in cartdict:
#                         cartdict[item.product.name]=item.quantity
#                     else:
#                         cartdict[item.product.name]+=item.quantity
#                 if cartdict[pdtobj.name]:

#                     remaining_quantity=pdtobj.quantity-cartdict[pdtobj.name]
#                 if not cartdict[pdtobj.name]:
#                     remaining_quantity=pdtobj.quantity

#                 print("***********",quantity,remaining_quantity)

#                 if int(quantity)>remaining_quantity:
#                     error="Product Out of Stock"
#                     # return render(request,"store/userdashboard/preview.html",{"error":error})
#                     return redirect(preview,someid)

     

#             cartadd=Cart(product=pdtobj,user=userobj,quantity=int(quantity),total=total)
#             cartadd.save()
#             return redirect(loggedincart) 
        


# def update_offer_price(request):
#     if request.method == "GET":
#         selected_offer = request.GET.get("offer") 
#         # pdtname=request.GET.get("pdtname") 
#         # print("###########",pdtname)
#         # offerobj=Productoffer.objects.get(offer_description=selected_offer)
#         # discount=offerobj.discount
#         # offer_price=productprice*
        

#          # Get the selected offer from the AJAX request

#         # Perform necessary calculations to update the offer price based on the selected offer
#         # Assuming you have the updated offer price as `new_offer_price`

#         response = {
#             "offer_price": 100
#         }
#         return JsonResponse(response)







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

    
    orderobj=Orders.objects.get(id=someid)
    product=orderobj.product
    product.quantity+=orderobj.quantity
    product.save()
    orderobj.orderstatus="Cancelled"
    orderobj.save()

    

    return JsonResponse({"message": "Confirm !","content":"Order Cancelled"})



def userprofile(request):
    # orderobjs=Orders.objects.all()
    username=request.session["username"]
    customerobj=Customers.objects.get(username=username)

    orderobjs=Orders.objects.filter(user=customerobj)
    
    addressobjs=Address.objects.filter(customer=customerobj)
    

    
    
    wishlistobjs=Wishlist.objects.filter(user=customerobj)

    cartobjs=Cart.objects.filter(user=customerobj)
    no_of_cart_items=cartobjs.count()
    
    no_of_wishlist_items=wishlistobjs.count()



    totalsum=0
    for item in cartobjs:
        totalsum+=item.total

    


    context={"orderobjs":orderobjs,"username":username,"addressobjs":addressobjs,"username":username,"addressobjs":addressobjs,"customerobj":customerobj,"cartobjs":cartobjs,"totalsum":totalsum,"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items}
    return render(request,"store/userdashboard/userprofile.html",context)


def edituserdetails(request):
    if request.method=="POST":
        name=request.POST["name"]
        name=request.POST["name"]
        email=request.POST["email"]
        phonenumber=request.POST["phonenumber"]
    
    customerobj=Customers.objects.get(username=request.session.get("username"))
    customerobj.name=name
    customerobj.email=email
    customerobj.phonenumber=phonenumber
    customerobj.save()
    return redirect(userprofile)

def edituseraddress(request,someid):
    if request.method=="POST":
        house=request.POST["house"]
        locality=request.POST["locality"]
        district=request.POST["district"]
        state=request.POST["state"]
        country=request.POST["country"]
        pincode=request.POST["pincode"]
    
    addressobj=Address.objects.get(id=someid)
    addressobj.house=house
    addressobj.locality=locality
    addressobj.district=district
    addressobj.state=state
    addressobj.country=country
    addressobj.pincode=pincode
    addressobj.save()
    return redirect(userprofile)

def deliveredproducts(request):
    username=request.session["username"]
    userobj=Customers.objects.get(username=username)
    orderobjs=Orders.objects.filter(user=userobj)
    wishlistobjs=Wishlist.objects.filter(user=userobj)

    cartobjs=Cart.objects.filter(user=userobj)
    no_of_cart_items=cartobjs.count()
    
    no_of_wishlist_items=wishlistobjs.count()



    totalsum=0
    for item in cartobjs:
        totalsum+=item.total
    context={"orderobjs":orderobjs,"totalsum":totalsum,"no_of_wishlist_items":no_of_wishlist_items,"no_of_cart_items":no_of_cart_items,"cartobjs":cartobjs}
    return render(request,"store/userdashboard/deliveredproducts.html",context)


def returnorder(request,orderid):
    orderobj=Orders.objects.get(id=orderid)
    orderobj.orderstatus="ReturnRequested"
    orderobj.save()
    return JsonResponse({"message":"Return Initiated"})


def addtowishlist(request):
    print("MWONEEE")
    productid=request.GET["productid"]
    
    user=Customers.objects.get(username=request.session["username"])
    try:
        wishlistobj=Wishlist.objects.get(product=Products.objects.get(id=productid),user=user) 
        if wishlistobj:
            message="Item already in wishlist"
            return JsonResponse({"alreadypresent":message})
    except:
        wishlistobj=Wishlist(product=Products.objects.get(id=productid),user=user)
        wishlistobj.save()
        message="Item added to wishlist"



    



        return JsonResponse({"added":message})
    

def wishlist(request):
    username=request.session["username"]
    user=Customers.objects.get(username=username)
    wishlistobjs=Wishlist.objects.filter(user=user)
    itemcount=wishlistobjs.count()

    cartobjs=Cart.objects.filter(user=user)
    no_of_cart_items=cartobjs.count()
    
    no_of_wishlist_items=wishlistobjs.count()



    totalsum=0
    for item in cartobjs:
        totalsum+=item.total

    context={"wishlistobjs":wishlistobjs,"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items,"cartobjs":cartobjs,"totalsum":totalsum,"itemcount":itemcount}
    return render(request,"store/userdashboard/wishlist.html",context)

def wishlistremove(request):
    username=request.session["username"]
    user=Customers.objects.get(username=username)
    productid=request.GET["productid"]
    productobj=Products.objects.get(id=productid)
    wishlistobj=Wishlist.objects.get(product=productobj,user=user)
    wishlistobj.delete()
    return JsonResponse({"message":"removed"})

def wishtocart(request):
    productid=request.GET["productid"]
    productobj=Products.objects.get(id=productid)
    username=request.session["username"]
    user=Customers.objects.get(username=username)
    wishlistobj=Wishlist.objects.get(user=user,product=productobj)
    try:
        cartobj=Cart.objects.get(user=user,product=productobj)
        if cartobj:
            cartobj.quantity+=1
            cartobj.total+=productobj.price
            cartobj.save()
    except:
        cartobj=Cart(user=user,product=productobj,quantity=1,total=productobj.price)
        cartobj.save()
        wishlistobj.delete()

    return JsonResponse({"message":"Added"})



def guestaddtowishlist(request):

    
    productid=request.GET["productid"]
    productid=str(productid)
    product=Products.objects.get(id=int(productid))
    productname=product.name
    image=product.image1.url
    price=float(product.price)

    wishlistdict=None
    added=None
    alreadypresent=None
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        print("DONNO",wishlistdict)

    if not wishlistdict:
        wishlistdict={}
        wishlistdict[productid]={"quantity":1,"productname":productname,"price":price,"image":image}
        added="Item added to wishlist"

    elif productid not in wishlistdict:
        wishlistdict[productid]={}
        wishlistdict[productid]["quantity"]=1
        wishlistdict[productid]["productname"]=productname
        wishlistdict[productid]["price"]=price
        wishlistdict[productid]["image"]=image
        added="Item added to wishlist"

    elif productid in wishlistdict:
        alreadypresent="Item already in wishlist"

    request.session["wishlistdict"]=wishlistdict
    print("DJUNGOO",wishlistdict)
    if added:
        return JsonResponse({"added":added})
    elif alreadypresent:
        return JsonResponse({"alreadypresent":alreadypresent})


def guestwishlist(request):
    
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        print("BLUNGOO",wishlistdict)
        
        if "cartdict" in request.session:
            cartdict=request.session["cartdict"]
            subtotal=0
            for k,v in cartdict.items():
                subtotal+=v["total"]
            cartcount=len(cartdict)
        else:
            cartdict={}
            subtotal=0
            cartcount=0
        if "wishlistdict" in request.session:
            wishlistdict=request.session["wishlistdict"]
            wishcount=len(wishlistdict) 
        else:
            wishcount=0  
        context={"wishlistdict":wishlistdict,"wishcount":wishcount,"cartcount":cartcount,"cartdict":cartdict}
        
        return render(request,"store/guestwishlist.html",context)

    else:
        message="Wishlist is Empty"
        context={"message":message}
        if "cartdict" in request.session:
            cartdict=request.session["cartdict"]
            subtotal=0
            for k,v in cartdict.items():
                subtotal+=v["total"]
            cartcount=len(cartdict)
        else:
            cartdict={}
            subtotal=0
            cartcount=0
        if "wishlistdict" in request.session:
            wishlistdict=request.session["wishlistdict"]
            wishcount=len(wishlistdict) 
        else:
            wishcount=0  
            wishlistdict={}
        
        context={"wishlistdict":wishlistdict,"wishcount":wishcount,"cartcount":cartcount,"cartdict":cartdict}
        return render(request,"store/guestwishlist.html",context)








    # username=request.session["username"]
    # user=Customers.objects.get(username=username)
    # wishlistobjs=Wishlist.objects.filter(user=user)
    # itemcount=wishlistobjs.count()

    # cartobjs=Cart.objects.filter(user=user)
    # no_of_cart_items=cartobjs.count()
    
    # no_of_wishlist_items=wishlistobjs.count()



    # totalsum=0
    # for item in cartobjs:
    #     totalsum+=item.total

    # context={"wishlistobjs":wishlistobjs,"no_of_cart_items":no_of_cart_items,"no_of_wishlist_items":no_of_wishlist_items,"cartobjs":cartobjs,"totalsum":totalsum,"itemcount":itemcount}
    # return render(request,"store/userdashboard/wishlist.html",context)


def guestwishlistremove(request):
    wishlistdict=request.session["wishlistdict"]
    productid=request.GET["productid"]
    del wishlistdict[str(productid)]
    request.session["wishlistdict"]=wishlistdict

    return JsonResponse({"removed":"removed"})

def guestwishtocart(request):
    print("FLINGO")
    productid=request.GET["productid"]
    wishlistdict=request.session["wishlistdict"]
    productname=wishlistdict[str(productid)]["productname"]
    price=wishlistdict[str(productid)]["price"]
    quantity=wishlistdict[str(productid)]["quantity"]
    image=wishlistdict[str(productid)]["image"]

    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        if str(productid) not in cartdict:
            cartdict[str(productid)]={}
            cartdict[str(productid)]["product"]=productname
            cartdict[str(productid)]["total"]=price
            cartdict[str(productid)]["quantity"]=quantity
            cartdict[str(productid)]["image"]=image
        else:
            
            cartdict[str(productid)]["product"]=productname
            cartdict[str(productid)]["total"]+=price
            cartdict[str(productid)]["quantity"]+=quantity
            cartdict[str(productid)]["image"]=image
        request.session["cartdict"]=cartdict



    else:
        request.session["cartdict"]={}
        cartdict=request.session["cartdict"]
        cartdict[str(productid)]={}
        cartdict[str(productid)]["product"]=productname
        cartdict[str(productid)]["quantity"]=quantity
        cartdict[str(productid)]["total"]=price
        cartdict[str(productid)]["image"]=image
        request.session["cartdict"]=cartdict


    del wishlistdict[str(productid)]
    request.session["wishlistdict"]=wishlistdict
    return JsonResponse({"messagge":"success"})


def razorupdateorder(request):
    
    
    username=request.session["username"]
    user=Customers.objects.get(username=username)
    cartobjs=Cart.objects.filter(user=user)
    
    for item in cartobjs:
         product=item.product
         orderdateobj=date.today()
         addressobj=Address.objects.get(customer=user,state="Kerala")
         orderobj=Orders(user=user,product=product,orderdate=orderdateobj,orderstatus="Ordered",ordertype="Razor Pay",quantity=item.quantity,finalprice=item.total,address=addressobj)
         orderobj.save()
        
    

    return JsonResponse({"message":"Done"})