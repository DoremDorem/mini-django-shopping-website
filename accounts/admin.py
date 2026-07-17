from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','last_login','date_joined','is_active')
    filter_horizontal=()
    list_filter=()
     # Right-side filters
    list_filter = (
        "is_active",
        "is_staff",
        "is_admin",
        "is_superadmin",
    )
    fieldsets = (
        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
            )
        }),

        ("Account Information", {
            "fields": (
                "email",
                "username",
                "password",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_admin",
                "is_superadmin",
            )
        }),
    )
    list_display_links=('email','first_name',"last_name",'username')
    readonly_fields=('last_login','date_joined')
    ordering=('-date_joined',)
admin.site.register(Account,AccountAdmin)