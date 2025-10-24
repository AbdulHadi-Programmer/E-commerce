from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from store.models import Customer


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = "Customer Profile"
    fk_name = "user"

class CustomUserAdmin(UserAdmin):
    inlines = (CustomerInline,)
    list_display = ("username", "email", "is_customer", "is_seller", "is_staff")
    list_filter = ("is_customer", "is_seller", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Roles", {"fields": ("is_customer", "is_seller")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(User, CustomUserAdmin)
