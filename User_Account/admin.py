from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import User_Reg,User_Change_Reg
from .models import CustomUser,user_address,cart



class CustomUserAdmin(UserAdmin):
    add_form = User_Reg
    form = User_Change_Reg
    model = CustomUser
    list_display = ('email', 'name', 'is_superuser',"is_staff", "is_active",)
 
    list_filter = ('is_superuser',)

    list_filter = ("email","name", "is_staff", "is_active",)
    

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','Phone')}),
        ('Permissions', {
            'fields': ("is_staff", "is_active", "groups", "user_permissions",),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff',"is_active", "groups", "user_permissions" )}
         ),
    )



    search_fields = ("email",'first_name')
    ordering = ('is_superuser',)   


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(user_address)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user","ID_Mobile","ID_Laptop","ID_Headphone","ID_Men","ID_Women","ID_Shoe","Quantity")
    



