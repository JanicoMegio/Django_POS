from django.contrib import admin
from posApp.models import Category, Products, Sales, salesItems, Inventoryrecord
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.unregister(Group)
#admin.site.unregister(Apscheduler)
#admin.site.register(Category)
#admin.site.register(Products)
#admin.site.register(Sales)
#admin.site.register(salesItems)
#admin.site.register(Employees)
#admin.site.register(Inventoryrecord)

