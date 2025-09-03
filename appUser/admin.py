from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organizer, Attendee


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Show these fields in list view
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)

    # Add "role" to the fieldsets so it appears in admin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)
