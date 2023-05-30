from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/",views.index,name="admin_index"),
    path("users/",views.users,name="admin_users"),
    path("products/",views.products,name="admin_products"),
    path("categories/",views.categories,name="admin_categories"),
    path("editproducts/<int:someid>/",views.editproducts,name="admin_editproducts"),
    path("deleteproducts/<int:someid>/",views.deleteproducts,name="admin_deleteproducts"),
    path("addproducts/",views.addproducts,name="admin_addproducts"),
    path("editcategories/<int:someid>/",views.editcategories,name="admin_editcategories"),
    path("deletecategories/<int:someid>/",views.deletecategories,name="admin_deletecategories"),
    path("addactegories/",views.addcategories,name="admin_addcategories"),
    path("blockuser/<int:someid>",views.blockuser,name="admin_blockuser"),
    path("unblockuser/<int:someid>",views.unblockuser,name="admin_unblockuser"),
    path("adminsignin/",views.adminsignin,name="admin_signin"),
    path("adminsignout/",views.adminsignout,name="admin_signout"),
    path("salesreport/",views.salesreport,name="salesreport"),
    path("downloadsales/",views.downloadsales,name="downloadsales"),
    



    path("orders/",views.orders,name="admin_orders"),
    path("editorderstatus/<int:someid>/",views.editorderstatus,name="admin_editorderstatus"),

    path("coupon/",views.coupon,name="coupon"),
    path("addcoupon/",views.addcoupon,name="addcoupon"),
    path("editcoupon/<int:couponid>",views.editcoupon,name="editcoupon"),
    path("deletecoupon/<int:couponid>",views.deletecoupon,name="deletecoupon"),


    path("categoryoffer/",views.categoryoffer,name="categoryoffer"),
    path("editcategoryoffer/<int:couponid>",views.editcategoryoffer,name="editcategoryoffer"),
    path("deletecategoryoffer/<int:offerid>",views.deletecategoryoffer,name="deletecategoryoffer"),




    path("productoffer/",views.productoffer,name="productoffer"),
    path("editproductoffer/<int:offerid>",views.editproductoffer,name="editproductoffer"),
    path("deleteproductoffer/<int:offerid>",views.deleteproductoffer,name="deleteproductoffer"),

    
    
]

