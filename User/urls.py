from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'User'

urlpatterns =[
    path('',views.checkpage,name='checkpage'),
    path('register/',views.RegisterPage,name='register'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.Logout,name='logout'),
    
    # main page starting
    path('category/',views.categorypage,name='category'),

    # description page
    path('description/<int:id>/',views.descriptionpage, name='description'),
    path('detaildesc/<int:id>/',views.detaildescpage,name='detaildesc'),
    
    #Buy now option id1 = brand id and id2 = user id
    path('buynow/<int:id1>/<int:id2>',views.buynowpage,name='buynow'),
    path('cartbuynow/<int:id>/',views.cartbuynow,name="cartbuynow"),

    # profile page id1 = brand id and id2 = user id
    path('profile/<int:id1>/<int:id2>/',views.profilepage,name="profile"),
    path('updateprofile/',views.updateprofpage,name="updateprofile"),
    path('checkoutprofile/<int:id>/',views.checkoutprofilepage,name='checkoutprofile'),

    # about us link
    path('contactus/',views.contactuspage,name='aboutus'),
    
    # resetpassword
    path('password-reset/',
    auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),
    name='password_reset'),

    path('password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
    name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
    name='password_reset_confirm'),
    
    path('reset/done/',
    auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
    name='password_reset_complete'),
    
    # Change password
    path('changepassword/',views.changepassword,name='changepassword'),

    # Add to cart
    path('cart/',views.cart,name='cart'),

    # Update Item
    path('updateitem/',views.updateItem,name='updateitem'),

    # Delete from cart
    path('deletefromcart/<int:id>/',views.deletefromcart,name='deletefromcart'),

    # success of the order
    path('sucess/<int:id1>/<int:id2>',views.successpage,name='success'),
    path('cartsuccess/<int:id>/',views.cartsuccesspage,name='cartsuccess')
]