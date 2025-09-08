from django.apps import AppConfig


class FbcBooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fbc_books'
    
    def ready(self):
        """
        Apply admin URL fix when Django is ready
        """
        try:
            from django.contrib.auth import get_user_model
            from django.urls import reverse, NoReverseMatch
            
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
                    if hasattr(self, 'view_name'):
                        try:
                            viewname = self.view_name.resolve(context)
                            if viewname.startswith('admin:auth_user_'):
                                action = viewname.split('_')[-1]
                                custom_url = f"admin:{CustomUser._meta.app_label}_{CustomUser._meta.model_name}_{action}"
                                try:
                                    return original_reverse(custom_url)
                                except NoReverseMatch:
                                    pass
                        except:
                            pass
                    
                    # Return empty string for missing URLs
                    return ''

            URLNode.render = safe_url_render
            
            print("Admin URL fix applied successfully!")
            
        except Exception as e:
            print(f"Could not apply admin URL fix: {e}")
            pass
