from django.shortcuts import render,redirect
from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.db import IntegrityError
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
        categorys=Category.objects.all()
        return render(request,"storeadmin/index.html",{"categorys":categorys})
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




def editproducts(request,someid):
    content=Products.objects.get(id=someid)
    if request.method=="POST":
        name=request.POST.get("name")
        price=request.POST.get("price")
        quantity=request.POST.get("quantity")
        category_name=request.POST.get("category")
        image1=request.POST.get("image")
        print(image1,"******")
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
            categoryobject=Category.objects.get(name=category_name)
            updated=Products(id=someid,name=name,price=price,quantity=quantity,category=categoryobject,description=description,image1=image1)
            updated.save()
            successmsg="Successfully Updated"
            return redirect(products)
        if error:
            return render(request,"storeadmin/products/editproducts.html",{"content":content,"error":error})

          


    return render(request,"storeadmin/products/editproducts.html",{"content":content})

def deleteproducts(request,someid):
    content=Products.objects.get(id=someid)
    if request.method=="POST":
        content.delete()
        return redirect(products)
    return render(request,"storeadmin/products/deleteproducts.html",{"content":content})

def addproducts(request):
    if request.method=="POST":
        name=request.POST.get("name")
        price=request.POST.get("price")
        quantity=request.POST.get("quantity")
        category_name=request.POST.get("category")
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
        elif category_name.isalpha==False:
            error="Category field can't have numbers"
        elif category_name not in Category.objects.filter(name=category_name).values_list('name', flat=True):
            error="Invalid category"
        elif len(description)<4:
            error="Description should contain minimum four characters"
        else:
            categoryobject=Category.objects.get(name=category_name)
            newproduct=Products(name=name,price=price,quantity=quantity,category=categoryobject,description=description)
            newproduct.save()
            return redirect(products)
        if error:
            return render(request,"storeadmin/products/addproducts.html",{"error":error})

    return render(request,"storeadmin/products/addproducts.html")
@never_cache
def categories(request):
    if "adminname" in request.session:
        datas=Category.objects.all()
        return render(request,"storeadmin/categories/categories.html",{"datas":datas})
    else:
        return redirect(adminsignin)

def editcategories(request,someid):
    obj=Category.objects.get(id=someid)
    if request.method=="POST":
        name=request.POST.get("name")
        items=request.POST.get("noofitems")
        if len(name)==0:
            error="Category name field can't be empty"
        elif name.isalpha()==False:
            error="Category name can;t be numbers"
        elif len(name)<4:
            error="Category name should atleast have 4 letters"
        elif len(name)>20:
            error="Category name can atmost can have 20 letters"
        else:
            edited=Category(id=someid,name=name,noofitems=items)
            edited.save()
            return redirect(categories)
        if error:
            return render(request,"storeadmin/categories/editcategories.html",{"obj":obj,"error":error})



        

    


    return render(request,"storeadmin/categories/editcategories.html",{"obj":obj})


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
    content.delete()



    all=Category.objects.all()
    for item in all:
        print(item.name,"$$$$$$$$$$$$$$$")





    return JsonResponse({"message": "Category deleted successfully."})
    

def addcategories(request):
    if request.method == "POST":
        name = request.POST.get("name")
        quantity=request.POST.get("quantity")
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
                added = Category(name=name,noofitems=quantity)
                added.save()
                return redirect(categories)
            except IntegrityError:
                error = "Category with this name already exists"

        return render(request, "storeadmin/categories/addcategories.html", {"error": error})

    return render(request, "storeadmin/categories/addcategories.html")




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

