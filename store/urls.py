from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("about/",views.about,name="about"),
    path("login/",views.login,name="login"),
    path("signup",views.signup,name="signup"),
    path("cart/",views.cart,name="cart"),
    path("shop/",views.shop,name="shop"),
    path("logout/",views.logout,name="logout"),
    path("blog/",views.blog,name="blog"),
    path("blog",views.contact,name="contact"),
    path("otplogin/",views.otplogin,name="otplogin"),
    path("verifyotp/",views.verifyotp,name="verifyotp"),
    # path("buynow/<int:someid>",views.buynow,name="buynow"),
    path("cancelorder/<int:someid>",views.cancelorder,name="cancelorder"),




    path("userprofile/",views.userprofile,name="userprofile"),
    path("edituserdetails/",views.edituserdetails,name="edituserdetails"),
    path("edituseraddress/<int:someid>",views.edituseraddress,name="edituseraddress"),





    path("loggedin/",views.loggedin,name="loggedin"),
    path("loggedinproduct/",views.loggedinproduct,name="loggedinproduct"),
    path("addtocart/<int:someid>",views.addtocart,name="addtocart"),
    path("preview/<int:someid>",views.preview,name="preview"),
    path("loggedincart/",views.loggedincart,name="loggedincart"),
    path("checkout/",views.checkout,name="checkout"),
    path("cashondelivery/",views.cashondelivery,name="cashondelivery"),
    path("previousorders/",views.previousorders,name="previousorders"),

    






    path("category_based_product/<int:someid>",views.category_based_product,name="category_based_product"),
    path("loggedincategory_based_product/<int:someid>",views.loggedincategory_based_product,name="loggedincategory_based_product"),


    path("deletecart/",views.deletecart,name="deletecart"),
    path("updatecart/<int:someid>",views.updatecart,name="updatecart"),



    

    # path("applycoupon/",views.applycoupon,name="applycoupon"),
    

]
