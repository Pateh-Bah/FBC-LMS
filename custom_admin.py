"""
Custom admin configuration to handle custom user model URLs properly.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe

# Remove the default User model from admin if it exists
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Custom admin site configuration
class CustomAdminSite(admin.AdminSite):
    site_header = "FBC Library System Administration"
    site_title = "FBC Library Admin"
    index_title = "Welcome to FBC Library Administration"
    
    def get_urls(self):
        """Override to handle custom user model URLs properly"""
        urls = super().get_urls()
        return urls

# Override the default admin site
admin.site.site_header = "FBC Library System Administration"
admin.site.site_title = "FBC Library Admin"
admin.site.index_title = "Welcome to FBC Library Administration"
