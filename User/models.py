from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
# Create your models here.

class Category(models.Model):
    def __str__(self):
        return self.category_name
    category_name = models.CharField(max_length=200)

class Beverage(models.Model):
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.SET_NULL)
    beverage_name =  models.CharField(max_length = 200)
    beverage_desc = models.CharField(max_length = 1000)
    beverage_price = models.IntegerField()
    beverage_image = models.CharField(max_length=500,blank= True,default = "https://images.unsplash.com/photo-1547595628-c61a29f496f0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60")

    def __str__(self):
        return self.beverage_name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    addressline1 = models.CharField(max_length = 200)
    addressline2 = models.CharField(max_length = 200)
    mobilenumber = models.CharField(max_length=10, validators = [RegexValidator(r'^\d{1,10}$')])
    pincode = models.CharField(max_length = 6 , validators = [RegexValidator(r'^\d{1,10}$')])
    state = models.CharField(max_length=50, default='Telangana')
    
    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
    

class Order(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
    complete = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    beverage = models.ForeignKey(Beverage,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(range(0,10), default=0,null=True,blank=True)

    @property
    def get_total(self):
        total = self.beverage.beverage_price * self.quantity
        return total