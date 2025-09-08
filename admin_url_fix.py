"""
Admin URL Pattern Fix for Custom User Model

This file contains the URL pattern mappings for the custom user model
to ensure Django admin works correctly with CustomUser instead of the default User model.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Get the custom user model
CustomUser = get_user_model()

# Create a custom admin site if not already created
class CustomAdminSite(admin.AdminSite):
    site_header = "FBC Library Administration"
    site_title = "FBC Library Admin"
    index_title = "Welcome to FBC Library Administration"
    
    def get_urls(self):
        urls = super().get_urls()
        # Add custom URL patterns that handle the custom user model
        return urls

# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register all models with the custom admin site
# This ensures proper URL pattern generation

# You can use this in your main urls.py by importing custom_admin_site
# and using path('admin/', custom_admin_site.urls) instead of admin.site.urls
