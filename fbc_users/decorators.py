"""
Custom authentication decorators for FBC Library System
Ensures strict database-backed authentication
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from fbc_users.models import CustomUser
import logging

logger = logging.getLogger(__name__)

def database_verified_login_required(view_func):
    """
    Decorator that ensures user is not only logged in but also exists and is active in database
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('fbc_users:login')
        
        try:
            # Force database lookup to verify user still exists and is valid
            db_user = CustomUser.objects.get(
                id=request.user.id,
                is_active=True
            )
            
            # Check if user is suspended
            if db_user.is_suspended:
                logger.warning(f"Suspended user {db_user.username} attempted to access {request.path}")
                logout(request)
                messages.error(request, 'Your account has been suspended.')
                return redirect('fbc_users:login')
            
            # Update request.user to ensure we have the latest data
            request.user = db_user
            
        except CustomUser.DoesNotExist:
            logger.warning(f"Non-existent user {request.user.id} attempted to access {request.path}")
            logout(request)
            messages.error(request, 'Your account is no longer valid. Please log in again.')
            return redirect('fbc_users:login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view

def user_type_required(allowed_types):
    """
    Decorator that restricts access to specific user types
    Usage: @user_type_required(['admin', 'staff'])
    """
    if isinstance(allowed_types, str):
        allowed_types = [allowed_types]
    
    def decorator(view_func):
        @wraps(view_func)
        @database_verified_login_required
        def wrapped_view(request, *args, **kwargs):
            if request.user.user_type not in allowed_types:
                logger.warning(
                    f"User {request.user.username} ({request.user.user_type}) "
                    f"attempted to access restricted view requiring {allowed_types}"
                )
                messages.error(
                    request, 
                    f'Access denied. This area is restricted to {", ".join(allowed_types)} users only.'
                )
                return redirect('fbc_books:dashboard')
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    return decorator

def admin_required(view_func):
    """Decorator for admin-only views"""
    return user_type_required('admin')(view_func)

def staff_or_admin_required(view_func):
    """Decorator for staff or admin views"""
    return user_type_required(['admin', 'staff'])(view_func)

def active_subscription_required(view_func):
    """
    Decorator that ensures user has an active subscription (for students accessing premium features)
    """
    @wraps(view_func)
    @database_verified_login_required
    def wrapped_view(request, *args, **kwargs):
        # Staff, lecturers, and admins always have access
        if request.user.user_type in ['staff', 'lecturer', 'admin']:
            return view_func(request, *args, **kwargs)
        
        # Students need active subscription
        if not request.user.subscription_status:
            messages.warning(
                request, 
                'This feature requires an active subscription. Please renew your subscription to continue.'
            )
            return redirect('fbc_payments:subscription')
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view
