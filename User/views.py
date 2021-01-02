from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

# confirm emails
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
 

# Create your views here.

# Checking page 
# this first command restricts from back button keep on above evry page u need to 
@login_required(login_url='User:login')
def Homepage(request):
    context={

    }
    return render(request, 'User/base.html',context)

# Registration of User using the forms
def RegisterPage(request):
    # if request.user.is_authenticated: 
    # retrun home page 
    # above two lines no need but just keep in mind if you need to restrict any page with out autherisation
    form = createuserform()

    if request.method == "POST":
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email1 = form.cleaned_data.get('email')
            messages.success(request,'Account created successfully for : ' + user)
            template = render_to_string('user/registeremailtemplate.html',{'user':user})
            email = EmailMessage(
                'Thank you. Account Confirmation!',
                template,
                settings.EMAIL_HOST_USER,
                [email1],
            )
            email.fail_silently = False
            email.send()
            return redirect('User:login')
    context={
        'form': form
    }
    return render(request,'user/register.html',context)

# Login page
def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('User:category')
        else: 
            messages.info(request,'Username or Password is incorrect')

    context={

    }
    return render(request,'user/login.html',context)

# logout page
def Logout(request):
    logout(request)
    return redirect('User:login')

# start page
def checkpage(request):
    context={

    }
    return render(request, 'user/check.html',context)

# Retrieving the information from the models and displaying all categories
def categorypage(request):
    category_list=Category.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user1=customer, complete=False)
        cartitems = order.get_cart_items
    else :
        cartitems = []
    
    context={
        'category_list':category_list,
        'cartitems':cartitems
    }
    return render(request, 'user/category.html',context)


# Retrieving the information from the models and displaying respective category items
def descriptionpage(request,id): 
    des = Beverage.objects.filter(category__id = id)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user1=customer, complete=False)
        cartitems = order.get_cart_items
    else :
        cartitems = []   
    context ={
        'des':des,
        'cartitems':cartitems 
    }
    return render(request,'user/description.html',context)

# detail description of the respective item
def detaildescpage(request,id):
    detaildesc = Beverage.objects.filter(id=id)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user1=customer, complete=False)
        cartitems = order.get_cart_items

    else :
        cartitems = []
    
    context={
        'detaildesc':detaildesc,
        'cartitems':cartitems
    }
    return render(request,'user/detaildesc.html',context)

# Commiting the changes for the user profile 
def updateprofpage(request):
    if request.method == 'POST':
        u_form = UserUpdateform(request.POST, instance=request.user)
        p_form = UpdateProfileform(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile had been updated')
            return redirect('User:category')

    else :
        u_form = UserUpdateform(instance=request.user)
        p_form = UpdateProfileform(instance=request.user.profile)

    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'user/updateprof.html',context)

# contact us
def contactuspage(request):
    context={

    }
    return render(request,'user/aboutus.html',context)

# Displays the profile of the User using forms, if only signed in as the user
@login_required(login_url='User:login')
def profilepage(request,id1,id2):

    if request.method == 'POST':
        u_form = UserUpdateform(request.POST, instance=request.user)
        p_form = UpdateProfileform(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request, f'Your profile has been updated')
            return redirect('User:buynow',id1=id1,id2=id2 )

    else :
        u_form = UserUpdateform(instance=request.user)
        p_form = UpdateProfileform(instance=request.user.profile)

    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'user/updateprofile.html',context)

# profile page of the User for checking out the order
def checkoutprofilepage(request,id):
    if request.method == 'POST':
        u_form = UserUpdateform(request.POST, instance=request.user)
        p_form = UpdateProfileform(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request, f'Your profile has been updated')
            return redirect('User:cartbuynow',id=id)

    else :
        u_form = UserUpdateform(instance=request.user)
        p_form = UpdateProfileform(instance=request.user.profile)

    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'user/updateprofile.html',context)

# Buy now option for the Cart functionality (Multiple items)
def cartbuynow(request,id):
    profile = Profile.objects.filter(user__id = id)
    customer = request.user
    order, created = Order.objects.get_or_create(user1=customer, complete=False)
    items = order.orderitem_set.all()
    cartitems = order.get_cart_items
    context={
        'items':items,
        'order':order,
        'profile':profile,
        'cartitems':cartitems
    }
    return render(request,'user/cartbuynow.html',context)

# Buy now option for the single item
@login_required(login_url='User:login')
def buynowpage(request,id1,id2):
    buy = Beverage.objects.filter(id=id1)
    profile = Profile.objects.filter(user__id = id2)
    customer = request.user
    order, created = Order.objects.get_or_create(user1=customer, complete=False)
    cartitems = order.get_cart_items
    context={
        'buy':buy,
        'profile':profile,
        'cartitems':cartitems
    } 
    return render(request,'user/buynow.html',context)

# Displays the cart details with required fields
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user1=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
    context={
        'items':items,
        'order':order,
        'cartitems':cartitems
    }
    return render(request,'user/cart.html',context)

# adding the item to the cart or the deleting from the cart manages in this section
def updateItem(request):
    data = json.loads(request.body)
    brandId = data['brandId']
    action = data['action']

    user = request.user
    brand = Beverage.objects.get(id=brandId)
    order, created = Order.objects.get_or_create(user1=user, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, beverage=brand)
    

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity + 1)

    orderitem.save()

    if orderitem.quantity<=0:
        orderitem.delete()

    messages.success(request, f'Your item had been added to cart')
    return JsonResponse('Item was added', safe=False)
    # return redirect('User:cart')

# RESET PASSWORD
def changepassword(request):
    if request.method=="POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, f'Your password is changed successfully')
            return redirect('User:category')
    elif request.method==None:
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(user=request.user)
        
    context = {
        'form':form
    }
    return render(request,'user/changepassword.html',context)

def deletefromcart(request,id):
    item = OrderItem.objects.filter(id=id)
    item.delete()
    return redirect('User:cart')

# Single item - Order confirmation through E-mail
def successpage(request,id1,id2):
    item = Beverage.objects.filter(id=id1)
    profile = Profile.objects.filter(user__id = id2)

    customer = request.user
    order, created = Order.objects.get_or_create(user1=customer, complete=False)
    cartitems = order.get_cart_items

    template = render_to_string('user/emailtemplate.html',{'item':item,'profile':profile})
    email = EmailMessage(
        'Thank you. Confirmation of order!',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently = False
    email.send()

    context = {
        'cartitems':cartitems
    }
    return render(request,'user/success.html',context)

# Cart items - order confirmation through E-mail
def cartsuccesspage(request,id):
    profile = Profile.objects.filter(user__id = id)
    customer = request.user
    order, created = Order.objects.get_or_create(user1=customer, complete=False)
    items = order.orderitem_set.all()
    

    template = render_to_string('user/cartemailtemplate.html',{'items':items,'profile':profile,'order':order})
    email = EmailMessage(
        'Thank you. Confirmation of order!',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently = False
    email.send()

    for item in items:
        item.delete()
    
    cartitems = order.get_cart_items
    context = {
        'cartitems':cartitems
    }
    return render(request,'user/success.html',context)