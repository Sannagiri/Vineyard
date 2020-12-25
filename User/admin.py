from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Beverage)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
