from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),

    path('adminregister', views.adminregister, name='adminregister'),
    path('admin_registration', views.admin_registration, name='admin_registration'),
    path('astoneadmin', views.astoneadmin, name='astoneadmin'),

    path('categories', views.categories, name='categories'),
    path('subcategories/<int:pk>/', views.subcategories, name='subcategories'),
    path('subproducts/<int:pk>/', views.subproducts, name='subproducts'),
    path('product/<int:pk>/', views.product, name='product'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('gallery', views.gallery, name='gallery'),
    path('products', views.products, name='products'),
    path('contactus', views.contactus, name='contactus'),
    path('contact_enquiry', views.contact_enquiry, name='contact_enquiry'),




    path('astoneadminhome', views.astoneadminhome, name='astoneadminhome'),   
    path('addproduct', views.addproduct, name='addproduct'),
    path('add_product', views.add_product, name='add_product'),
    path('view_product', views.view_product, name='view_product'),
    path('view_rewards', views.view_rewards, name='view_rewards'),
    path('viewmyrewards', views.viewmyrewards, name='viewmyrewards'),
    path('view_users', views.view_users, name='view_users'),
    path('add_category', views.add_category, name='add_category'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('subcategory', views.subcategory, name='subcategory'),
    path('add_subcategory', views.add_subcategory, name='add_subcategory'),
    path('edit_subcategory/<int:pk>/', views.edit_subcategory, name='edit_subcategory'),
    path('delete_subcategory/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),

    path('editproduct/<int:pk>/', views.editproduct, name='editproduct'),

    path('viewusersingle/<int:pk>/', views.viewusersingle, name='viewusersingle'),
    path('viewproductsingle/<int:pk>/', views.viewproductsingle, name='viewproductsingle'),

    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),

    path('view_unsoldproducts', views.view_unsoldproducts, name='view_unsoldproducts'),
    path('update_reward/<int:pk>/', views.update_reward, name='update_reward'),
    path('search/', views.search_products, name='search_products'),


    path('viewusersingle2/<referral_code>/', views.viewusersingle2, name='viewusersingle2'),
    path('delete_productimage/<int:pk>/', views.delete_productimage, name='delete_productimage'),

    path('edit_productimage/<int:pk>/', views.edit_productimage, name='edit_productimage'),
    path('addproductimage', views.addproductimage, name='addproductimage'),
    path('add_productimage', views.add_productimage, name='add_productimage'),
    path('view_paidrewards', views.view_paidrewards, name='view_paidrewards'),
    path('view_supercustomer', views.view_supercustomer, name='view_supercustomer'),
    path('make_supercustomer/<int:pk>/', views.make_supercustomer, name='make_supercustomer'),
    path('make_normalcustomer/<int:pk>/', views.make_normalcustomer, name='make_normalcustomer'),
    path('delete_user1/<int:pk>/', views.delete_user1, name='delete_user1'),
    path('delete_user2/<int:pk>/', views.delete_user2, name='delete_user2'),

    path('delete_staff/<int:pk>/', views.delete_staff, name='delete_staff'),
    path('add_staff', views.add_staff, name='add_staff'),
    path('view_referral', views.view_referral, name='view_referral'),
    path('addstaff', views.addstaff, name='addstaff'),
    path('view_staff', views.view_staff, name='view_staff'),
    path('astonestaff', views.astonestaff, name='astonestaff'),
    path('otp_verification', views.otp_verification, name='otp_verification'),
    path('otp_login_verification', views.otp_login_verification, name='otp_login_verification'),

    path('view_commissions', views.view_commissions, name='view_commissions'),


    path('registration', views.registration, name='registration'),
    path('registration_success', views.registration_success, name='registration_success'),
    path('customer_registration', views.customer_registration, name='customer_registration'),
    path('customer_login', views.customer_login, name='customer_login'),
    path('customer_home', views.customer_home, name='customer_home'),
    path("SignOut",views.SignOut,name="SignOut"),
    path("SignOut2",views.SignOut2,name="SignOut2"),

    path('update_commission/<int:pk>/', views.update_commission, name='update_commission'),

    path('update_profile/<int:pk>/', views.update_profile, name='update_profile'),
    path("qrcodescanner",views.qrcodescanner,name="qrcodescanner"),
    path("reward",views.reward,name="reward"),
    path('addReward', views.addReward, name='addReward'),
    path('view_soldproducts', views.view_soldproducts, name='view_soldproducts'),
    path('referralpayment', views.referralpayment, name='referralpayment'),

    path('viewmyreferrals', views.viewmyreferrals, name='viewmyreferrals'),
    path('enquiry', views.enquiry, name='enquiry'),
    path('viewallcategories', views.viewallcategories, name='viewallcategories'),
    path('viewsubcategories/<int:pk>/', views.viewsubcategories, name='viewsubcategories'),
    path('viewsubproducts/<int:pk>/', views.viewsubproducts, name='viewsubproducts'),
    path('viewproductsingleuser/<int:pk>/', views.viewproductsingleuser, name='viewproductsingleuser'),
    path('add_to_pdf_cart', views.add_to_pdf_cart, name='add_to_pdf_cart'),

    # path('add_to_pdf_cart/<int:pk>/', views.add_to_pdf_cart, name='add_to_pdf_cart'),
    path('make_pdf', views.make_pdf, name='make_pdf'),
    path('delete_pdf', views.delete_pdf, name='delete_pdf'),
    path('delete_soldproducts', views.delete_soldproducts, name='delete_soldproducts'),
    path('delete_singlepdf/<int:pk>/', views.delete_singlepdf, name='delete_singlepdf'),

    path('view_requests', views.view_requests, name='view_requests'),
    path('viewrewardrequestsingle/<int:pk>/', views.viewrewardrequestsingle, name='viewrewardrequestsingle'),
    path('update_request/<int:pk>/', views.update_request, name='update_request'),
    path('delete_request/<int:pk>/', views.delete_request, name='delete_request'),

    path('cash_error', views.cash_error, name='cash_error'),

    path('view_transactions', views.view_transactions, name='view_transactions'),

    path('withdaw_done', views.withdaw_done, name='withdaw_done'),
    path('withdraw_request', views.withdraw_request, name='withdraw_request'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('viewallproductsuser', views.viewallproductsuser, name='viewallproductsuser'),
    path('enquiry_form', views.enquiry_form, name='enquiry_form'),
    path('view_enquiry', views.view_enquiry, name='view_enquiry'),
    # path('pdf/<int:pk>/', views.customer_render_pdf_view, name='customer-pdf-view'),
    path('pdf2', views.pdf2, name='pdf2'),

    path('pdf', views.customer_render_pdf_view, name='customer-pdf-view'),


]