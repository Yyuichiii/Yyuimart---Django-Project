from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import User_Reg,User_Change_Reg
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = User_Reg
    form = User_Change_Reg
    model = CustomUser
    list_display = ('email', 'first_name', 'is_superuser',"is_staff", "is_active",)
 
    list_filter = ('is_superuser',)

    list_filter = ("email","first_name", "is_staff", "is_active",)
    

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {
            'fields': ("is_staff", "is_active", "groups", "user_permissions",),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_root',"is_active", "groups", "user_permissions" )}
         ),
    )



    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)