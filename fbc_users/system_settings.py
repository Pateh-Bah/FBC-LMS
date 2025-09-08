from django.db import models

class SystemSettings(models.Model):
    system_name = models.CharField(max_length=100, default="FBC Library System", help_text="Name of the library system")
    primary_color = models.CharField(max_length=7, default="#00843D", help_text="Hex code for FBC Green or chosen primary color.")
    
    # Additional color customization fields
    sidebar_color = models.CharField(max_length=7, default="#28a745", help_text="Color for the sidebar navigation")
    header_color = models.CharField(max_length=7, default="#343a40", help_text="Color for the header navigation")
    footer_color = models.CharField(max_length=7, default="#6c757d", help_text="Color for the footer section")
    
    favicon = models.ImageField(upload_to='system/', null=True, blank=True, help_text="Site favicon (small icon)")
    logo = models.ImageField(upload_to='system/', null=True, blank=True, help_text="System logo for sidebar and header")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"System Settings ({self.system_name})"

    @classmethod
    def get_settings(cls):
        settings = cls.objects.first()
        if not settings:
            settings = cls.objects.create()
        return settings

    @classmethod
    def get_primary_color(cls):
        settings = cls.get_settings()
        return settings.primary_color
    
    @classmethod
    def get_sidebar_color(cls):
        settings = cls.get_settings()
        return settings.sidebar_color
    
    @classmethod
    def get_header_color(cls):
        settings = cls.get_settings()
        return settings.header_color
    
    @classmethod
    def get_footer_color(cls):
        settings = cls.get_settings()
        return settings.footer_color

    @classmethod
    def get_system_name(cls):
        settings = cls.get_settings()
        return settings.system_name

    @classmethod
    def get_logo_url(cls):
        settings = cls.get_settings()
        return settings.logo.url if settings.logo else None

    @classmethod
    def get_favicon_url(cls):
        settings = cls.get_settings()
        return settings.favicon.url if settings.favicon else None
