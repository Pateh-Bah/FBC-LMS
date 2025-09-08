from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.urls import reverse, NoReverseMatch

class SafeForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    """
    Custom ForeignKeyRawIdWidget that handles missing URL patterns gracefully.
    """
    def url_for_value(self, value):
        """Override to handle NoReverseMatch gracefully"""
        try:
            return super().url_for_value(value)
        except NoReverseMatch:
            return None
