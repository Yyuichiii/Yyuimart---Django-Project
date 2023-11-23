from django.contrib import admin
from .models import Mobile

# Register your models here.
@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ("PID","Brand", "PName","Price","Quantity")
    search_fields = ("Brand__startswith","PName__startswith","PID__startswith", )




