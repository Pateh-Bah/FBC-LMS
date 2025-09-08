from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser
from .system_settings import SystemSettings


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "user_type",
        "university_id",
        "is_suspended",
        "is_subscription_active",
        "subscription_end_date",
        "profile_image_preview",
    )
    
    list_filter = (
        "user_type",
        "is_suspended",
        "is_active",
        "is_subscription_active",
    )
    
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "university_id",
    )
    
    ordering = ("username",)
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "email", "phone_number")}
        ),
        (
            "Library Info",
            {
                "fields": (
                    "user_type",
                    "university_id",
                    "is_suspended",
                    "is_subscription_active",
                    "subscription_end_date",
                    "profile_image",
                )
            }
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")}
        ),
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_image.url)
        return "No image"
    profile_image_preview.short_description = "Profile Image"
    
    # Allow filtering by subscription status
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter + ("is_subscription_active",)
        return self.list_filter
    
    # Custom actions
    actions = ["activate_subscription", "deactivate_subscription"]
    
    def activate_subscription(self, request, queryset):
        queryset.update(is_subscription_active=True)
    activate_subscription.short_description = "Activate subscription for selected users"
    
    def deactivate_subscription(self, request, queryset):
        queryset.update(is_subscription_active=False)
    deactivate_subscription.short_description = "Deactivate subscription for selected users"

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ("primary_color", "updated_at")
    fields = ("primary_color",)
    search_fields = ("primary_color",)
    ordering = ("-updated_at",)
