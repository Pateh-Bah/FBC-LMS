"""
Enhanced Authentication Middleware for FBC Library System
Ensures all user authentication is strictly database-backed
"""

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from fbc_users.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class DatabaseAuthenticationEnforcementMiddleware(MiddlewareMixin):
    """
    Middleware to ensure all authenticated users are verified against the database
    and that no in-memory or cached authentication bypasses database verification
    """
    
    # URLs that don't require authentication
    EXEMPT_URLS = [
        '/users/login/',
        '/admin/login/',
        '/static/',
        '/media/',
    ]
    
    def process_request(self, request):
        """
        Process each request to ensure authenticated users are database-verified
        """
        # Skip for exempt URLs
        if any(request.path.startswith(url) for url in self.EXEMPT_URLS):
            return None
        
        # If user is authenticated, verify they still exist in database
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Force a database query to verify user exists
                db_user = CustomUser.objects.get(
                    id=request.user.id,
                    is_active=True
                )
                
                # Check if user is suspended
                if db_user.is_suspended:
                    logger.warning(f"Suspended user {db_user.username} attempted access")
                    logout(request)
                    messages.error(request, 'Your account has been suspended. Please contact the administrator.')
                    return redirect('fbc_users:login')
                
                # Update last activity
                db_user.last_activity = timezone.now()
                db_user.save(update_fields=['last_activity'])
                
            except CustomUser.DoesNotExist:
                # User no longer exists in database - force logout
                logger.warning(f"Non-existent user {request.user.id} attempted access")
                logout(request)
                messages.error(request, 'Your account is no longer valid. Please log in again.')
                return redirect('fbc_users:login')
        
        return None

class StrictUserTypeEnforcementMiddleware(MiddlewareMixin):
    """
    Middleware to enforce user type restrictions on specific URLs
    """
    
    # Define URL patterns and required user types
    USER_TYPE_RESTRICTIONS = {
        '/admin/': ['admin'],
        '/fbc_books/admin/': ['admin'],
        '/fbc_users/admin/': ['admin'],
        '/fbc_fines/staff/': ['admin', 'staff'],
        '/fbc_payments/staff/': ['admin', 'staff'],
    }
    
    def process_request(self, request):
        """
        Check if user has proper permissions for the requested URL
        """
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return None
        
        # Check each restriction
        for url_pattern, allowed_types in self.USER_TYPE_RESTRICTIONS.items():
            if request.path.startswith(url_pattern):
                if request.user.user_type not in allowed_types:
                    logger.warning(
                        f"User {request.user.username} ({request.user.user_type}) "
                        f"attempted to access restricted URL: {request.path}"
                    )
                    messages.error(
                        request, 
                        f'Access denied. This area is restricted to {", ".join(allowed_types)} users only.'
                    )
                    return redirect('fbc_books:dashboard')
        
        return None

class AuditTrailMiddleware(MiddlewareMixin):
    """
    Middleware to log all authentication-related activities for audit purposes
    """
    
    def process_request(self, request):
        """
        Log important authentication events
        """
        # Log login attempts
        if request.path == '/users/login/' and request.method == 'POST':
            username = request.POST.get('username', 'unknown')
            logger.info(f"Login attempt for username: {username} from IP: {self.get_client_ip(request)}")
        
        # Log admin access
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            logger.info(f"Admin access by {request.user.username} to {request.path}")
        
        return None
    
    def get_client_ip(self, request):
        """Get the client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
