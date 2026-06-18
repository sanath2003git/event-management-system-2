from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User, Organizer, Attendee


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        "profile_preview",
        "username",
        "email",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = (
        "username",
    )


    fieldsets = BaseUserAdmin.fieldsets + (

        (

            "Additional Information",

            {

                "fields": (

                    "role",

                    "profile_pic",

                )

            },

        ),

    )


    add_fieldsets = BaseUserAdmin.add_fieldsets + (

        (

            "Additional Information",

            {

                "fields": (

                    "role",

                    "profile_pic",

                )

            },

        ),

    )


    def profile_preview(self, obj):

        if obj.profile_pic:

            return format_html(

                '<img src="{}" width="40" height="40" style="border-radius:50%; object-fit:cover;" />',

                obj.profile_pic.url

            )

        return "-"


    profile_preview.short_description = "Profile"



@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):

    list_display = (

        "profile_preview",

        "username",

        "email",

        "is_active",

    )


    search_fields = (

        "username",

        "email",

    )


    ordering = (

        "username",

    )


    def profile_preview(self, obj):

        if obj.profile_pic:

            return format_html(

                '<img src="{}" width="40" height="40" style="border-radius:50%; object-fit:cover;" />',

                obj.profile_pic.url

            )

        return "-"


    profile_preview.short_description = "Profile"



@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):

    list_display = (

        "profile_preview",

        "username",

        "email",

        "is_active",

    )


    search_fields = (

        "username",

        "email",

    )


    ordering = (

        "username",

    )


    def profile_preview(self, obj):

        if obj.profile_pic:

            return format_html(

                '<img src="{}" width="40" height="40" style="border-radius:50%; object-fit:cover;" />',

                obj.profile_pic.url

            )

        return "-"


    profile_preview.short_description = "Profile"