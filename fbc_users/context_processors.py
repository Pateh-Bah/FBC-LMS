from fbc_users.system_settings import SystemSettings
from django.conf import settings as django_settings


def system_settings_context(request):
    """Return UI/system theme/context values plus safe public Supabase values.

    Note: we intentionally do NOT expose SUPABASE_SERVICE_ROLE_KEY here. Only
    the public anon key and base URL are surfaced for client-side usage when
    needed.
    """
    try:
        settings = SystemSettings.get_settings()
        return {
            'primary_color': settings.primary_color,
            'sidebar_color': settings.sidebar_color,
            'header_color': settings.header_color,
            'footer_color': settings.footer_color,
            'system_name': settings.system_name,
            'system_logo': settings.logo.url if settings.logo else None,
            'system_favicon': settings.favicon.url if settings.favicon else None,
            # Expose only public Supabase values (anon key + url) to templates
            'supabase_url': getattr(django_settings, 'SUPABASE_URL', None),
            'supabase_anon_key': getattr(django_settings, 'SUPABASE_ANON_KEY', None),
        }
    except Exception:
        # Return default values if there's an error
        return {
            'primary_color': '#22c55e',
            'sidebar_color': '#16a34a',
            'header_color': '#15803d',
            'footer_color': '#166534',
            'system_name': 'FBC Library System',
            'system_logo': None,
            'system_favicon': None,
            'supabase_url': getattr(django_settings, 'SUPABASE_URL', None),
            'supabase_anon_key': getattr(django_settings, 'SUPABASE_ANON_KEY', None),
        }
