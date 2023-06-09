from django.shortcuts import render,redirect
from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError
import os



from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import xlsxwriter



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
            top_returned_product=None
            top_product=None

            orderdict={}
            for item in orderobjs:
                if item.product.name not in orderdict:
                    orderdict[item.product.name]=item.quantity
                else:
                    orderdict[item.product.name]+=item.quantity
            try:
                top_count = max(orderdict.values())
            except:
                pass
            for key,value in orderdict.items():
                if value==top_count:
                    top_product=key
                    break
            
            #Most Returned Products Graph logic
            returninitiatedobjs=Orders.objects.filter(orderstatus="Returned")
            returndict={}
            for i in returninitiatedobjs:
                if i.product.name not in returndict:
                    returndict[i.product.name]=1
                else:
                    returndict[i.product.name]+=1
            try:
                top_returned_count=max(returndict.values())
            except:
                pass

            for key,value in returndict.items():
                if value==top_returned_count:
                    top_returned_product=key


            


            return render(request,"storeadmin/index.html",{"orderdict":orderdict,"returndict":returndict,      "top_product":top_product,"top_count":top_count,"top_returned_product":top_returned_product})
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
            # datas=Customers.objects.filter(username=enteredname)
            datas = Customers.objects.filter(username__icontains=enteredname)
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
            datas=Products.objects.filter(name__icontains=enteredproduct)
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
    error={}
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
            error["name"]="Productname should contain minimum four characters"
        elif len(name)>20:
            error["name"]="Username can only have upto 20 characters"
        elif name.isalpha()==False:
            error["name"]="Productname can't have numbers" 
        elif price.isalpha()==True:
            error["price"]="Price can't have letters"
        elif quantity.isalpha()==True:
            error["quantity"]="Quantity can't have letters"
        elif category_name.isalpha==False:
            error["category"]="Category field can't have numbers"
        elif category_name not in Category.objects.filter(name=category_name).values_list('name', flat=True):
            error["category"]="Invalid category"
        elif len(description)<4:
            error["description"]="Description should contain minimum four characters"
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
            return render(request,"storeadmin/products/addproducts.html",{"error":error,"categoryobjs":categoryobjs,     "name":name,"price":price,"quantity":quantity,"description":description})

    return render(request,"storeadmin/products/addproducts.html",{"categoryobjs":categoryobjs})
@never_cache
def categories(request):
    if "adminname" in request.session:
        datas=Category.objects.all()
        if request.method=="POST":
            enteredname=request.POST["searchitem"]
            datas=Category.objects.filter(name__icontains=enteredname)
        
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
def blockcategories(request, someid):
    print(someid,"SOMEID ***********")
    

    content = Category.objects.get(id=someid)
    print(content.name,"CONTENT###########################")
    if content.isblocked==True:
        content.isblocked=False
        content.save()
        return redirect(categories)
    elif content.isblocked==False:
        content.isblocked=True
        content.save()
        return redirect(categories)

# def unblockcategories(request):
#     categoryid=request.GET["categoryid"]
#     categoryobj = Category.objects.get(id=categoryid)
    
#     categoryobj.isblocked=False
#     categoryobj.save()
#     print("DONEE")
#     return JsonResponse({"message": "Unblocked","offerid":categoryid})

# def blockcategories(request):
#     categoryid=request.GET["categoryid"]
#     categoryobj = Category.objects.get(id=categoryid)

#     if categoryobj.isblocked==True:
#         categoryobj.isblocked=False
#         categoryobj.save()
#         return JsonResponse({"message": "Unblocked"})
#     elif categoryobj.isblocked==False:
#         categoryobj.isblocked=True
#         categoryobj.save()
#         return JsonResponse({"message": "Blocked"})
    
    # categoryobj.isblocked=True
    # categoryobj.save()
    # return JsonResponse({"message": "Blocked","offerid":categoryid})



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
    if request.method=="POST":
        entereddate=request.POST["searchitem"]
        orderobjs=Orders.objects.filter(orderdate__icontains=entereddate)


    return render(request,"storeadmin/orders/orders.html",{"orderobjs":orderobjs})


def editorderstatus(request,someid):

    if request.method=="POST":
        orderobj=Orders.objects.get(id=someid)
        orderstatus=request.POST.get("orderstatus")
        if orderstatus=="Returned":
            pdtobj=orderobj.product
            pdtobj.quantity+=orderobj.quantity
            pdtobj.save()
        
        orderobj.orderstatus=orderstatus


        
        orderobj.save()
        return redirect(orders)

    return render(request,"storeadmin/orders/editorderstatus.html")



def salesreport(request):
    if request.method=="POST":
        if "show" in request.POST:
            start_date=request.POST.get("start_date")
            end_date=request.POST.get("end_date")
            orderobjs = Orders.objects.filter(orderdate__range=[start_date, end_date])
            if orderobjs.count()==0:
                message="Sorry! No orders in this particular date range"
                context={"orderobjs":orderobjs,"message":message}
            else:

                context={"orderobjs":orderobjs}
            return render(request,"storeadmin/salesreport.html",context)
        elif "download" in request.POST:
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter)
            elements = []

            # Add heading
            styles = getSampleStyleSheet()
            heading_style = styles['Heading1']
            heading = "Sales Report"
            heading_paragraph = Paragraph(heading, heading_style)
            elements.append(heading_paragraph)
            elements.append(Spacer(1, 12))  # Add space after heading

            ords = Orders.objects.filter(orderdate__range=[start_date, end_date])
            

            if ords:
                data = [['Sl.No.', 'Name', 'Product', 'House', 'Order Date', 'Order Status', 'Quantity']]
                slno = 0
                for ord in ords:
                    slno += 1
                    row = [slno, ord.user.name, ord.product.name, ord.address.house, ord.orderdate, ord.orderstatus, ord.quantity]
                    data.append(row)

                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))

                elements.append(table)
            else:
                elements.append(Paragraph("No orders", styles['Normal']))
            if elements:

                doc.build(elements)
                buf.seek(0)
                return FileResponse(buf, as_attachment=True, filename='Orders.pdf')
        
        elif "downloadinexcel" in request.POST:

            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")



            ords = Orders.objects.filter(orderdate__range=[start_date, end_date])

            # Create Excel workbook and worksheet
            workbook = xlsxwriter.Workbook("Sales_Report.xlsx")
            worksheet = workbook.add_worksheet('Sales Report')

            # Write the table headers
            headers = ['Sl.No.', 'Name', 'Product', 'House', 'Order Date', 'Order Status', 'Quantity']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            # Write the data rows
            row = 1
            for slno, ord in enumerate(ords, start=1):
                worksheet.write(row, 0, slno)
                worksheet.write(row, 1, ord.user.name)
                worksheet.write(row, 2, ord.product.name)
                worksheet.write(row, 3, ord.address.house)
                worksheet.write(row, 4, str(ord.orderdate))
                worksheet.write(row, 5, ord.orderstatus)
                worksheet.write(row, 6, ord.quantity)
                row += 1

            workbook.close()

            # Create a file-like buffer to receive the workbook data
            buf = io.BytesIO()
            
            buf.seek(0)
            

            # Return the Excel file as a FileResponse
            return FileResponse(buf, as_attachment=True, filename='Sales_Report.xlsx', content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')



    
    

    
    return render(request,"storeadmin/salesreport.html")





# def downloadsales(request):
#     start_date_str = request.GET.get('start_date')
#     end_date_str = request.GET.get('end_date')

#     start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
#     end_date = datetime.strptime(end_date_str, "%Y-%m-%d")



#     buf=io.BytesIO()
#     c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
#     textobj=c.beginText()
#     textobj.setTextOrigin(inch,inch)
#     textobj.setFont("Helvetica",14)


#     heading = "Sales Report"
#     textobj.textLine(heading)
#     textobj.textLine("-" * len(heading))

#     ords = Orders.objects.filter(orderdate__range=[start_date, end_date])
#     # customer=Customers.objects.get(username=request.session["username"])


#     if ords:
#         lines=[]
#         slno=0
#         for ord in ords:
#             slno+=1
#             orderdetails=f"{slno}.{ord.user.name},{ord.product.name},{ord.address.house},{ord.orderdate},{ord.orderstatus},{ord.quantity} "
#             lines.append(orderdetails)
#     else:
#         lines=["No orders"]

    




   
#     for line in lines:
#         textobj.textLine(line)

#     c.drawText(textobj)
#     c.showPage()
#     c.save()
#     buf.seek(0)
#     return FileResponse(buf,as_attachment=True,filename='Orders.pdf')


# def downloadsales(request):
#     start_date_str = request.GET.get('start_date')
#     end_date_str = request.GET.get('end_date')

#     start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
#     end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

#     buf = io.BytesIO()
#     doc = SimpleDocTemplate(buf, pagesize=letter)
#     elements = []

#     # Add heading
#     styles = getSampleStyleSheet()
#     heading_style = styles['Heading1']
#     heading = "Sales Report"
#     heading_paragraph = Paragraph(heading, heading_style)
#     elements.append(heading_paragraph)
#     elements.append(Spacer(1, 12))  # Add space after heading

#     ords = Orders.objects.filter(orderdate__range=[start_date, end_date])
    

#     if ords:
#         data = [['Sl.No.', 'Name', 'Product', 'House', 'Order Date', 'Order Status', 'Quantity']]
#         slno = 0
#         for ord in ords:
#             slno += 1
#             row = [slno, ord.user.name, ord.product.name, ord.address.house, ord.orderdate, ord.orderstatus, ord.quantity]
#             data.append(row)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, 0), 12),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
#             ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#             ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 1), (-1, -1), 10),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ]))

#         elements.append(table)
#     else:
#         elements.append(Paragraph("No orders", styles['Normal']))
#     if elements:

#         doc.build(elements)
#         buf.seek(0)
#         return FileResponse(buf, as_attachment=True, filename='Orders.pdf')
        

def coupon(request):  
    couponobjs=Coupon.objects.all()
    if request.method=="POST":
            enteredcoupon=request.POST.get("searchitem")
            couponobjs=Coupon.objects.filter(code__icontains=enteredcoupon)
            return render(request,"storeadmin/coupons/coupons.html",{"couponobjs":couponobjs})
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
    if request.method=="POST":
            enteredoffer=request.POST.get("searchitem")
            catofferobjs=Categoryoffer.objects.filter(offer_description__icontains=enteredoffer)
            context={"catofferobjs":catofferobjs}
            return render(request,"storeadmin/categoryoffer/categoryoffer.html",context)

    context={"catofferobjs":catofferobjs}
    return render(request,"storeadmin/categoryoffer/categoryoffer.html",context)

def addcategoryoffer(request):
    
    categoryobjs=Category.objects.all()
    context={"categoryobjs":categoryobjs}

    if request.method=="POST":
        categoryname=request.POST["categoryname"]
        offer=request.POST["offer"]
        discount=request.POST["discount"]
       
  
        categoryobj=Category.objects.get(name=categoryname)
        catofferobj=Categoryoffer(category=categoryobj,offer_description=offer,discount=discount)
        catofferobj.save()
        return redirect(categoryoffer)
    return render(request,"storeadmin/categoryoffer/addcategoryoffer.html",context)

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
    if request.method=="POST":
            enteredoffer=request.POST.get("searchitem")
            pdtofferobjs=Productoffer.objects.filter(offer_description__icontains=enteredoffer)
            context={"pdtofferobjs":pdtofferobjs}
            return render(request,"storeadmin/productoffer/productoffer.html",context)

    context={"pdtofferobjs":pdtofferobjs}
    return render(request,"storeadmin/productoffer/productoffer.html",context)

def addproductoffer(request):
    
    productobjs=Products.objects.all()
    context={"productobjs":productobjs}

    if request.method=="POST":
        productname=request.POST["productname"]
        offer=request.POST["offer"]
        discount=request.POST["discount"]


        productobj=Products.objects.get(name=productname)
        productofferobj=Productoffer(product=productobj,offer_description=offer,discount=discount)
        productofferobj.save()
        return redirect(productoffer)
    return render(request,"storeadmin/productoffer/addproductoffer.html",context)


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