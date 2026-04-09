from django.contrib import admin
from django.utils.html import format_html

from .models import Address, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "profile_preview")
    search_fields = ("user__username", "user__email", "phone_number")

    def profile_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.profile_image.url)
        return "No image"

    profile_preview.short_description = "Image"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "label", "city", "state", "is_default")
    list_filter = ("city", "state", "country", "is_default")
    search_fields = ("full_name", "user__username", "phone_number")
    autocomplete_fields = ("user",)
