from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("about/",views.about,name="about"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("cart/",views.cart,name="cart"),
    path("shop/",views.shop,name="shop"),
    path("logout/",views.logout,name="logout"),
    path("blog/",views.blog,name="blog"),
    path("blog",views.contact,name="contact"),
    path("otplogin/",views.otplogin,name="otplogin"),
    path("verifyotp/",views.verifyotp,name="verifyotp"),
    # path("buynow/<int:someid>",views.buynow,name="buynow"),
    path("cancelorder/<int:someid>",views.cancelorder,name="cancelorder"),
    path("returnorder/<int:orderid>",views.returnorder,name="returnorder"),




    path("userprofile/",views.userprofile,name="userprofile"),
    path("edituserdetails/",views.edituserdetails,name="edituserdetails"),
    path("edituseraddress/<int:someid>",views.edituseraddress,name="edituseraddress"),
    path("deliveredproducts/",views.deliveredproducts,name="deliveredproducts"),





    path("loggedin/",views.loggedin,name="loggedin"),
    path("loggedinproduct/",views.loggedinproduct,name="loggedinproduct"),
    path("loggedincontact/",views.loggedincontact,name="loggedincontact"),
    path("loggedinabout/",views.loggedinabout,name="loggedinabout"),
    # path("addtocart/<int:someid>",views.addtocart,name="addtocart"),
    path("preview/<int:someid>",views.preview,name="preview"),
    path("loggedincart/",views.loggedincart,name="loggedincart"),
    path("deletecartitem/",views.deletecartitem,name="deletecartitem"),
    path("quantityupdate/",views.quantityupdate,name="quantityupdate"),
    path("guestquantityupdate/",views.guestquantityupdate,name="guestquantityupdate"),
    path("guestdeletecartitem/",views.guestdeletecartitem,name="guestdeletecartitem"),



    path("checkout/",views.checkout,name="checkout"),
    path("cashondelivery/",views.cashondelivery,name="cashondelivery"),
    path("previousorders/",views.previousorders,name="previousorders"),

    






    path("category_based_product/<int:someid>",views.category_based_product,name="category_based_product"),
    path("loggedincategory_based_product/<int:someid>",views.loggedincategory_based_product,name="loggedincategory_based_product"),


    path("deletecart/",views.deletecart,name="deletecart"),
    path("updatecart/<int:someid>",views.updatecart,name="updatecart"),
    path("increasequantity/<int:itemid>",views.increasequantity,name="increasequantity"),
    

    path("applycouponajax/",views.applycouponajax,name="applycouponajax"),

    # path("update_offer_price/",views.update_offer_price,name="update_offer_price")

    

    # path("applycoupon/",views.applycoupon,name="applycoupon"),

    path("guestpreview/<int:someid>",views.guestpreview,name="guestpreview"),
    path("guestcart/",views.guestcart,name="guestcart"),




    path("filtercategory/<int:someid>",views.filtercategory,name="filtercategory"),
    path("filterprice/<int:someid>",views.filterprice,name="filterprice"),

    path("guestfiltercategory/<int:someid>",views.guestfiltercategory,name="guestfiltercategory"),
    path("guestfilterprice/<int:someid>",views.guestfilterprice,name="guestfilterprice"),
   
    

]
