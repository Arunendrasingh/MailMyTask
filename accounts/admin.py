from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from accounts.models import CustomUser

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "email", "contact", "is_superuser"]
    list_filter = ["is_superuser", "is_active"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": [
         "first_name", "last_name", "contact", "date_of_birth"]}),
        ("Permissions", {"fields": ["is_superuser", "is_staff_user", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "contact", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "first_name", "last_name", "contact"]
    ordering = ["id", "email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)

# admin.site.unregister(Group)
