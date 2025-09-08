"""
URL configuration for library_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""       
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Redirects for old admin URLs (must come before admin/ to catch them)
    path('admin/dashboard/', RedirectView.as_view(url='/dashboard/admin/', permanent=True)),
    path('admin/manage-books/', RedirectView.as_view(url='/manage/books/', permanent=True)),
    path('admin/manage-users/', RedirectView.as_view(url='/manage/users/', permanent=True)),
    path('admin/manage-borrowings/', RedirectView.as_view(url='/manage/borrowings/', permanent=True)),
    path('admin/attendance-log/', RedirectView.as_view(url='/manage/attendance-log/', permanent=True)),
    
    path('admin/', admin.site.urls),
    path('users/', include('fbc_users.urls')),  # namespace already defined in urls.py
    path('fines/', include('fbc_fines.urls')),  # namespace already defined in urls.py
    path('notifications/', include('fbc_notifications.urls')),  # namespace already defined in urls.py
    path('payments/', include('fbc_payments.urls')),  # namespace already defined in urls.py
    path('', include('fbc_books.urls')),  # Root URLs handled by fbc_books
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)