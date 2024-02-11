from django.contrib import admin
from .models import Mobile,Laptop,HeadPhone,Men,Women,Shoe

# Register your models here.
@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ("PID","Brand", "PName","Price","Category")
    search_fields = ("Brand__startswith","PName__startswith","PID__startswith", )

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ("PID","Brand", "PName","Price","Category")
    search_fields = ("Brand__startswith","PName__startswith","PID__startswith", )

@admin.register(HeadPhone)
class HeadPhoneAdmin(admin.ModelAdmin):
    list_display = ("PID","Brand", "PName","Price","Category")
    search_fields = ("Brand__startswith","PName__startswith","PID__startswith", )

@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    list_display = ("PID","Brand", "PName","Price","Category")
    search_fields = ("Brand__startswith","PName__startswith","PID__startswith", )

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ("PID","Brand", "PName","Price","Category")
    search_fields = ("Brand__startswith","PName__startswith","PID__startswith", )

@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ("PID","Brand", "PName","Price","Category")
    search_fields = ("Brand__startswith","PName__startswith","PID__startswith", )





