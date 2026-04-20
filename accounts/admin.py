from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # This shows the role directly in the list of users
    list_display = ('username', 'email', 'role', 'is_staff')
    
    # fieldsets controls the "Edit User" page
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Profile Info', {
            'fields': ('role', 'phone_number', 'bio', 'profile_picture')
        }),
    )
    
    # add_fieldsets controls the "Add User" page
    # We must ensure the structure is: (Title, {'fields': (tuple_of_fields)})
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Assignment', {
            'fields': ('role', 'phone_number')
        }),
    )

admin.site.register(User, CustomUserAdmin)