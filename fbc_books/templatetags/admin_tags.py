from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def safe_admin_url(url_name, *args, **kwargs):
    """
    Safely generate admin URLs, returning None if the URL doesn't exist.
    This prevents NoReverseMatch errors for custom user models.
    """
    try:
        return reverse(url_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return None

@register.simple_tag
def safe_url(url_name, *args, **kwargs):
    """
    Safely generate URLs, returning None if the URL doesn't exist.
    """
    try:
        return reverse(url_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return None
