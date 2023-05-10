from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("about/",views.about,name="about"),
    path("login/",views.login,name="login"),
    path("signup",views.signup,name="signup"),
    path("cart/",views.cart,name="cart"),
    path("shop/",views.shop,name="shop"),
    path("loggedin/",views.loggedin,name="loggedin"),
    path("loggedinproduct/",views.loggedinproduct,name="loggedinproduct"),
    path("logout/",views.logout,name="logout"),
    path("blog/",views.blog,name="blog"),
    path("blog",views.contact,name="contact"),
    path("otplogin/",views.otplogin,name="otplogin"),
    path("verifyotp/",views.verifyotp,name="verifyotp"),
    path("buynow/<int:someid>",views.buynow,name="buynow"),
    

]
