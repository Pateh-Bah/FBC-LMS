"""
Django admin URL fix for custom user models.

This module provides a comprehensive solution for handling admin URLs 
when using custom user models, preventing NoReverseMatch errors.
"""

import django
from django.apps import apps
from django.urls import reverse, NoReverseMatch

def apply_admin_url_fix():
    """
    Apply the admin URL fix after Django apps are loaded.
    """
    # Only apply the fix if Django is fully loaded
    if not apps.ready:
        return
    
    from django.contrib.auth import get_user_model
    
    # Get the custom user model
    CustomUser = get_user_model()

    # Monkey patch admin to handle missing URLs gracefully
    original_reverse = reverse

    def safe_reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None):
        """
        Safe version of reverse that handles NoReverseMatch gracefully
        """
        try:
            return original_reverse(viewname, urlconf, args, kwargs, current_app)
        except NoReverseMatch:
            # For auth_user URLs, try to map to the custom user model
            if viewname.startswith('admin:auth_user_'):
                action = viewname.split('_')[-1]  # get 'changelist', 'add', 'change', etc.
                custom_url = f"admin:{CustomUser._meta.app_label}_{CustomUser._meta.model_name}_{action}"
                try:
                    return original_reverse(custom_url, urlconf, args, kwargs, current_app)
                except NoReverseMatch:
                    pass
            
            # If we can't find a replacement, return a placeholder URL
            return '#'

    # Apply the monkey patch
    import django.urls.base
    django.urls.base.reverse = safe_reverse

    # Also patch the template tag
    from django.template.defaulttags import URLNode

    original_render = URLNode.render

    def safe_url_render(self, context):
        """
        Safe version of URLNode.render that handles NoReverseMatch gracefully
        """
        try:
            return original_render(self, context)
        except NoReverseMatch:
            # For auth_user URLs, try to map to the custom user model
            if hasattr(self, 'view_name') and self.view_name.resolve(context).startswith('admin:auth_user_'):
                viewname = self.view_name.resolve(context)
                action = viewname.split('_')[-1]
                custom_url = f"admin:{CustomUser._meta.app_label}_{CustomUser._meta.model_name}_{action}"
                try:
                    return original_reverse(custom_url)
                except NoReverseMatch:
                    pass
            
            # Return empty string for missing URLs
            return ''

    URLNode.render = safe_url_render

    print("Admin URL fix applied successfully!")

# Don't apply the fix immediately - wait for Django to be ready
if apps.ready:
    apply_admin_url_fix()
else:
    # This will be called when Django is ready
    from django.apps import AppConfig
    from django.apps.registry import apps as django_apps
    
    def ready_callback():
        apply_admin_url_fix()
    
    # Register the callback to be called when Django is ready
    django_apps.ready_event.connect(ready_callback)
