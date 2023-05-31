from django.shortcuts import render,redirect
from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.db import IntegrityError
import os



from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import datetime



# Create your views here.
@never_cache
def adminsignin(request):
    if "adminname" in request.session:
        return redirect(index)

    if request.method=="POST":
        un=request.POST.get("username")
        pw=request.POST.get("password")
        obj=authenticate(username=un,password=pw)
        if obj is not None:
            request.session["adminname"]=un
            return redirect(index)
        else:
            error="Invalid Credentials"
            return render(request,"storeadmin/adminsignin.html",{"error":error})

    return render(request,"storeadmin/adminsignin.html")
@never_cache
def index(request):
    if "adminname" in request.session:
        orderobjs=Orders.objects.all()
        orderdict={}
        for item in orderobjs:
            if item.product.name not in orderdict:
                orderdict[item.product.name]=item.quantity
            else:
                orderdict[item.product.name]+=item.quantity
        top_count = max(orderdict.values())
        for key,value in orderdict.items():
            if value==top_count:
                top_product=key
                break
           
        print(orderdict,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")    
        return render(request,"storeadmin/index.html",{"orderdict":orderdict,"top_product":top_product,"top_count":top_count})
    else:
        return redirect(adminsignin)
@never_cache  
def adminsignout(request):
    if 'adminname' in request.session:
        request.session.flush()   
    return redirect(adminsignin)
   
@never_cache
def users(request):
    if "adminname" in request.session:
        datas=Customers.objects.all()
        if request.method=="POST":
            enteredname=request.POST.get("searchitem")
            datas=Customers.objects.filter(username=enteredname)
            return render(request,"storeadmin/users/users.html",{"datas":datas})
        return render(request,"storeadmin/users/users.html",{"datas":datas})
    else:
        return redirect(adminsignin)

def blockuser(request,someid):
    obj=Customers.objects.get(id=someid)
    obj.isblocked=True
    obj.save()
    return redirect(users)

def unblockuser(request,someid):
    obj=Customers.objects.get(id=someid)
    obj.isblocked=False
    obj.save()
    return redirect(users)








@never_cache
def products(request):
    if "adminname" in request.session:
        datas=Products.objects.all()
        if request.method=="POST":
            enteredproduct=request.POST.get("searchitem")
            datas=Products.objects.filter(name=enteredproduct)
            return render(request,"storeadmin/products/products.html",{"datas":datas})
        return render(request,"storeadmin/products/products.html",{"datas":datas})
    else:
        return redirect(adminsignin)




# def edit(request, product_id):
#     prod = get_object_or_404(Product, product_id=product_id)

#     if request.method == 'POST':
#         prod.name = request.POST.get('name')
#         prod.description = request.POST.get('description')
#         prod.price = request.POST.get('price')

#         # Check if new images are provided
#         if 'image1' in request.FILES:
#             # Delete the existing image1 file
#             if prod.image1:
#                 os.remove(prod.image1.path)
#             prod.image1 = request.FILES.get('image1')

#         if 'image2' in request.FILES:
#             # Delete the existing image2 file
#             if prod.image2:
#                 os.remove(prod.image2.path)
#             prod.image2 = request.FILES.get('image2')

#         if 'image3' in request.FILES:
#             # Delete the existing image3 file
#             if prod.image3:
#                 os.remove(prod.image3.path)
#             prod.image3 = request.FILES.get('image3')

#         category_name = request.POST.get('catogery')

#         # Retrieve the category if it exists, otherwise assign a default category
#         cat_obj, _ = category.objects.get_or_create(name=category_name)

#         prod.catogery = cat_obj

#         prod.save()
#         return redirect('productview')
#     else:
#         context = {'prod': prod}
#         return render(request, 'edit.html', context)


#ARUN'S CODE
def editproducts(request, someid):
    content=Products.objects.get(id=someid)
    categoryobjs=Category.objects.all()

    if request.method == 'POST':
        name=request.POST.get("name")
        price=request.POST.get("price")
        quantity=request.POST.get("quantity")
        category_name=request.POST.get("category")
        # image1=request.FILES.get("image")
        # print(image1,"******")
        description=request.POST.get("description")
        if len(name)<4:
            error="Productname should contain minimum four characters"
        elif len(name)>20:
            error="Username can only have upto 20 characters"
        elif name.isalpha()==False:
            error="Productname can't have numbers" 
        elif price.isalpha()==True:
            error="Price can't have letters"
        elif quantity.isalpha()==True:
            error="Quantity can't have letters"
        # elif category.isalpha==False:
        #     error="Category field can't have numbers"
        elif len(description)<4:
            error="Description should contain minimum four characters"
        else:




            content.name = request.POST.get('name')
            content.description = request.POST.get('description')
            content.price = request.POST.get('price')
            content.quantity=quantity

            # Check if new images are provided
            if 'image1' in request.FILES:
                # Delete the existing image1 file
                if content.image1:
                    os.remove(content.image1.path)
                content.image1 = request.FILES.get('image1')

            if 'image2' in request.FILES:
                # Delete the existing image2 file
                if content.image2:
                    os.remove(content.image2.path)
                content.image2 = request.FILES.get('image2')

            if 'image3' in request.FILES:
                # Delete the existing image3 file
                if content.image3:
                    os.remove(content.image3.path)
                content.image3 = request.FILES.get('image3')

            if 'image4' in request.FILES:
                # Delete the existing image3 file
                if content.image4:
                    os.remove(content.image4.path)
                content.image4 = request.FILES.get('image4')

            # category_name = request.POST.get('category')

            # Retrieve the category if it exists, otherwise assign a default category
            categoryobject=Category.objects.get(name=category_name)

            content.category = categoryobject

            content.save()
            return redirect(products)
        if error:
            return render(request,"storeadmin/products/editproducts.html",{"content":content,"error":error,"categoryobjs":categoryobjs})

    return render(request,"storeadmin/products/editproducts.html",{"content":content,"categoryobjs":categoryobjs})





# MYCODE

# def editproducts(request,someid):
#     content=Products.objects.get(id=someid)
#     if request.method=="POST":
#         name=request.POST.get("name")
#         price=request.POST.get("price")
#         quantity=request.POST.get("quantity")
#         category_name=request.POST.get("category")
#         # image1=request.FILES.get("image")
#         # print(image1,"******")
#         description=request.POST.get("description")
#         if len(name)<4:
#             error="Productname should contain minimum four characters"
#         elif len(name)>20:
#             error="Username can only have upto 20 characters"
#         elif name.isalpha()==False:
#             error="Productname can't have numbers" 
#         elif price.isalpha()==True:
#             error="Price can't have letters"
#         elif quantity.isalpha()==True:
#             error="Quantity can't have letters"
#         # elif category.isalpha==False:
#         #     error="Category field can't have numbers"
#         elif len(description)<4:
#             error="Description should contain minimum four characters"
#         else:
#             categoryobject=Category.objects.get(name=category_name)

#             if 'image1' in request.FILES:
#             # Delete the existing image1 file
#                 if content.image1:
#                     os.remove(content.image1.path)
#                     updatedimage1 = request.FILES.get('image1')


#             if 'image2' in request.FILES:
#             # Delete the existing image1 file
#                 if content.image2:
#                     os.remove(content.image4.path)
#                     updatedimage2 = request.FILES.get('image2')

#             if 'image3' in request.FILES:
#             # Delete the existing image1 file
#                 if content.image3:
#                     os.remove(content.image3.path)
#                     updatedimage3 = request.FILES.get('image3')
#             if 'image4' in request.FILES:
#             # Delete the existing image1 file
#                 if content.image4:
#                     os.remove(content.image4.path)
#                 updatedimage4 = request.FILES.get('image4')



#             updated=Products(id=someid,name=name,price=price,quantity=quantity,category=categoryobject,description=description,image1=updatedimage1,image2=updatedimage2,image3=updatedimage3,image4=updatedimage4)
#             updated.save()
#             successmsg="Successfully Updated"
#             return redirect(products)
#         if error:
#             return render(request,"storeadmin/products/editproducts.html",{"content":content,"error":error})

          


#     return render(request,"storeadmin/products/editproducts.html",{"content":content})
def deleteproducts(request, someid):
    print(someid,"SOMEID ***********")
    

    content = Products.objects.get(id=someid)
    print(content.name,"CONTENT###########################")
    content.delete()



    # all=Category.objects.all()
    # for item in all:
    #     print(item.name,"$$$$$$$$$$$$$$$")





    return JsonResponse({"message": "Product deleted successfully."})



# def deleteproducts(request,someid):
#     content=Products.objects.get(id=someid)
#     if request.method=="POST":
#         content.delete()
#         return redirect(products)
#     return render(request,"storeadmin/products/deleteproducts.html",{"content":content})

def addproducts(request):
    categoryobjs=Category.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        price=request.POST.get("price")
        quantity=request.POST.get("quantity")
        category_name=request.POST.get("category")
        description=request.POST.get("description")
        image1=request.FILES.get("image1")
        image2=request.FILES.get("image2")
        image3=request.FILES.get("image3")
        image4=request.FILES.get("image4")
        if len(name)<4:
            error="Productname should contain minimum four characters"
        elif len(name)>20:
            error="Username can only have upto 20 characters"
        elif name.isalpha()==False:
            error="Productname can't have numbers" 
        elif price.isalpha()==True:
            error="Price can't have letters"
        elif quantity.isalpha()==True:
            error="Quantity can't have letters"
        elif category_name.isalpha==False:
            error="Category field can't have numbers"
        elif category_name not in Category.objects.filter(name=category_name).values_list('name', flat=True):
            error="Invalid category"
        elif len(description)<4:
            error="Description should contain minimum four characters"
        else:
            categoryobject=Category.objects.get(name=category_name)
            product = Products.objects.create(
            name=name,
            category=categoryobject,
            description=description,
            quantity=quantity,
            price=price,
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4)            
            # newproduct=Products(name=name,price=price,quantity=quantity,category=categoryobject,description=description,image1=image1,image2=image2,image3=image3,image4=image4)
            # newproduct.save()
            return redirect(products)
        if error:
            return render(request,"storeadmin/products/addproducts.html",{"error":error,"categoryobjs":categoryobjs})

    return render(request,"storeadmin/products/addproducts.html",{"categoryobjs":categoryobjs})
@never_cache
def categories(request):
    if "adminname" in request.session:
        datas=Category.objects.all()
        return render(request,"storeadmin/categories/categories.html",{"datas":datas})
    else:
        return redirect(adminsignin)

def editcategories(request,someid):
    obj=Category.objects.get(id=someid)
    categoryobjs=Category.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        items=request.POST.get("noofitems")
        if len(name)==0:
            error="Category name field can't be empty"
        elif name.isalpha()==False:
            error="Category name can;t be numbers"
        elif len(name)<4:
            error="Category name should atleast have 4 letters"
        elif Category.objects.filter(name=name):
            error="Same Category name is not allowed"
        elif len(name)>20:
            error="Category name can atmost can have 20 letters"
        else:
            obj.name=name
            obj.noofitems=items
            if 'image' in request.FILES:
                # Delete the existing image1 file
                if obj.image:
                    os.remove(obj.image.path)
                obj.image = request.FILES.get('image')
            obj.save()
            # edited=Category(id=someid,name=name,noofitems=items)
            # edited.save()
            return redirect(categories)
        if error:
            return render(request,"storeadmin/categories/editcategories.html",{"obj":obj,"error":error,"categoryobjs":categoryobjs})



        

    


    return render(request,"storeadmin/categories/editcategories.html",{"obj":obj,"categoryobjs":categoryobjs})


# def deletecategories(request,someid):
#     content=Category.objects.get(id=someid)
#     if request.method=="POST":
#         content.delete()
#         return redirect(categories)
#     return render(request,"storeadmin/categories/deletecategories.html",{"content":content})
def deletecategories(request, someid):
    print(someid,"SOMEID ***********")
    

    content = Category.objects.get(id=someid)
    print(content.name,"CONTENT###########################")
    if content.isblocked==True:
        content.isblocked=False
        content.save()
    elif content.isblocked==False:
        content.isblocked=True
        content.save()



    # all=Category.objects.all()
    # for item in all:
    #     print(item.name,"$$$$$$$$$$$$$$$")





    return JsonResponse({"message": "Category updated successfully."})
    

def addcategories(request):
    categoryobjs=Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        quantity=request.POST.get("quantity")
        image=request.FILES.get("image")
        if len(name) == 0:
            error = "Category name field can't be empty"
        elif not name.isalpha():
            error = "Category name can't be numbers"
        elif len(name) < 4:
            error = "Category name should have at least 4 letters"
        elif len(name) > 20:
            error = "Category name can have at most 20 letters"
        else:
            try:
                added = Category(name=name,noofitems=quantity,image=image)
                added.save()
                return redirect(categories)
            except IntegrityError:
                error = "Category with this name already exists"

        return render(request, "storeadmin/categories/addcategories.html", {"error": error})

    return render(request, "storeadmin/categories/addcategories.html",{"categoryobjs":categoryobjs})




# def addcategories(request):
#     if request.method=="POST":   
#         name=request.POST.get("name")
#         if len(name)==0:
#             error="Category name field can't be empty"
#         elif name.isalpha()==False:
#             error="Category name can't be numbers"
#         elif len(name)<4:
#             error="Category name should atleast have 4 letters"
#         elif len(name)>20:
#             error="Category name can atmost can have 20 letters"
#         else:
#             try:

#                 added=Category(name=name)
#                 added.save()
#                 return redirect(categories)
#             except IntegrityError:
#                 duplicate="Duplicate category not allowed"
#                 return render(request,"storeadmin/categories/addcategories.html",{"duplicate":duplicate})

#         if error:
#             return render(request,"storeadmin/categories/addcategories.html",{"error":error})

#     return render(request,"storeadmin/categories/addcategories.html")


def orders(request):
    orderobjs=Orders.objects.all()


    return render(request,"storeadmin/orders/orders.html",{"orderobjs":orderobjs})


def editorderstatus(request,someid):

    if request.method=="POST":
        orderobj=Orders.objects.get(id=someid)
        orderstatus=request.POST.get("orderstatus")
        orderobj.orderstatus=orderstatus

        
        orderobj.save()
        return redirect(orders)

    return render(request,"storeadmin/orders/editorderstatus.html")



def salesreport(request):
    


    return render(request,"storeadmin/salesreport.html")


def downloadsales(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")



    buf=io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textobj=c.beginText()
    textobj.setTextOrigin(inch,inch)
    textobj.setFont("Helvetica",14)

    ords = Orders.objects.filter(orderdate__range=[start_date, end_date])
    customer=Customers.objects.get(username=request.session["username"])


    if ords:
        lines=[]
        slno=0
        for ord in ords:
            slno+=1
            orderdetails=f"{slno},{ord.user.name},{ord.product.name},{ord.address.house},{ord.orderdate},{ord.orderstatus},{ord.quantity} "
            lines.append(orderdetails)
    else:
        lines=["No orders"]






   
    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename='Orders.pdf')
    

def coupon(request):  
    couponobjs=Coupon.objects.all()
    return render(request,"storeadmin/coupons/coupons.html",{"couponobjs":couponobjs})

def addcoupon(request):

    if request.method=="POST":

        code=request.POST["code"]
        discount_percent=request.POST["discount_percent"]
        minprice=request.POST["minprice"]
        maxprice=request.POST["maxprice"]
        isavailable=request.POST["isavailable"]
        print("DEIIIII",isavailable)
        if isavailable=="Yes":
            isavailable=True
        else:
            isavailable=False
        coup=Coupon(code=code,discount_percentage=discount_percent,minprice=minprice,maxprice=maxprice,isavailable=isavailable)
        coup.save()
        return redirect(coupon)
    return render(request,"storeadmin/coupons/addcoupons.html")

def editcoupon(request,couponid):
    couponobj=Coupon.objects.get(id=couponid)
    
    if request.method=="POST":

        
        code=request.POST["code"]
        discount_percentage=request.POST["discount_percentage"]
        minprice=request.POST["minprice"]
        maxprice=request.POST["maxprice"]
        isavailable=request.POST["isavailable"]
        if isavailable=="Yes":
            isavailable=True
        else:
            isavailable=False
        

        couponobj.code=code
        couponobj.discount_percentage=discount_percentage
        couponobj.minprice=minprice
        couponobj.maxprice=maxprice
        couponobj.isavailable=isavailable
        couponobj.save()



        return redirect(coupon)
    context={"couponobj":couponobj}
    return render(request,"storeadmin/coupons/editcoupon.html",context)

def deletecoupon(request,couponid):
    couponobj=Coupon.objects.get(id=couponid)
    couponobj.delete()

    return JsonResponse({"message":"Deleted"})


def categoryoffer(request):
    catofferobjs=Categoryoffer.objects.all()

    context={"catofferobjs":catofferobjs}
    return render(request,"storeadmin/categoryoffer/categoryoffer.html",context)

def editcategoryoffer(request,offerid):
    catofferobj=Categoryoffer.objects.get(id=offerid)
    categoryobjs=Category.objects.all()
    if request.method=="POST":

        
        categoryname=request.POST["categoryname"]
        offer_description=request.POST["offer_description"]
        discount=request.POST["discount"]
        categoryobj=Category.objects.get(name=categoryname)

        catofferobj.category=categoryobj
        catofferobj.offer_description=offer_description
        catofferobj.discount=discount
        catofferobj.save()



        return redirect(categoryoffer)
    context={"catofferobj":catofferobj,"categoryobjs":categoryobjs}
    return render(request,"storeadmin/categoryoffer/editcategoryoffer.html",context)



def deletecategoryoffer(request,offerid):
    catofferobj=Categoryoffer.objects.get(id=offerid)
    catofferobj.delete()

    return JsonResponse({"message":"Deleted"})





def productoffer(request):
    pdtofferobjs=Productoffer.objects.all()

    context={"pdtofferobjs":pdtofferobjs}
    return render(request,"storeadmin/productoffer/productoffer.html",context)


def editproductoffer(request,offerid):
    pdtofferobj=Productoffer.objects.get(id=offerid)
    productobjs=Products.objects.all()
    if request.method=="POST":

        
        productname=request.POST["productname"]
        offer_description=request.POST["offer_description"]
        discount=request.POST["discount"]
        productobj=Products.objects.get(name=productname)

        pdtofferobj.product=productobj
        pdtofferobj.offer_description=offer_description
        pdtofferobj.discount=discount
        pdtofferobj.save()



        return redirect(productoffer)
    context={"pdtofferobj":pdtofferobj,"productobjs":productobjs}
    return render(request,"storeadmin/productoffer/editproductoffer.html",context)


def deleteproductoffer(request,offerid):
    pdtofferobj=Productoffer.objects.get(id=offerid)
    pdtofferobj.delete()

    return JsonResponse({"message":"Deleted"})