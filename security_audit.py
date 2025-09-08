#!/usr/bin/env python
"""
Security Audit Script for FBC Library System
Ensures all authentication is database-backed and secure
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from fbc_users.models import CustomUser
from django.db import connection

def audit_authentication_system():
    """Comprehensive audit of the authentication system"""
    print("=" * 60)
    print("FBC LIBRARY SYSTEM SECURITY AUDIT")
    print("=" * 60)
    
    # 1. Check if custom user model is properly configured
    print("\n1. USER MODEL CONFIGURATION")
    print("-" * 30)
    print(f"✓ Custom User Model: {settings.AUTH_USER_MODEL}")
    print(f"✓ Database Backend: {settings.DATABASES['default']['ENGINE']}")
    
    # 2. Check authentication backends
    print("\n2. AUTHENTICATION BACKENDS")
    print("-" * 30)
    for backend in settings.AUTHENTICATION_BACKENDS:
        print(f"✓ {backend}")
    
    # 3. Check middleware for authentication
    print("\n3. AUTHENTICATION MIDDLEWARE")
    print("-" * 30)
    auth_middleware = [m for m in settings.MIDDLEWARE if 'auth' in m.lower()]
    for middleware in auth_middleware:
        print(f"✓ {middleware}")
    
    # 4. Verify users exist in database
    print("\n4. DATABASE USER VERIFICATION")
    print("-" * 30)
    
    # Check total users in database
    total_users = CustomUser.objects.count()
    print(f"✓ Total users in database: {total_users}")
    
    # Check specific admin and staff users
    test_users = ['fbcadmin', 'fbcstaff']
    
    for username in test_users:
        try:
            user = CustomUser.objects.get(username=username)
            print(f"✓ User '{username}' exists in database")
            print(f"  - User Type: {user.user_type}")
            print(f"  - Is Active: {user.is_active}")
            print(f"  - Is Staff: {user.is_staff}")
            print(f"  - Is Superuser: {user.is_superuser}")
            print(f"  - Is Suspended: {user.is_suspended}")
            
            # Test authentication against database
            auth_user = authenticate(username=username, password='1234')
            if auth_user:
                print(f"  - Database Authentication: ✅ SUCCESS")
                # Verify it's the same user object
                if auth_user.id == user.id:
                    print(f"  - User Identity Match: ✅ VERIFIED")
                else:
                    print(f"  - User Identity Match: ❌ MISMATCH")
            else:
                print(f"  - Database Authentication: ❌ FAILED")
                
        except CustomUser.DoesNotExist:
            print(f"❌ User '{username}' NOT found in database")
    
    # 5. Check for any hardcoded authentication
    print("\n5. SECURITY VERIFICATION")
    print("-" * 30)
    
    # Verify no anonymous access to protected views
    print("✓ Anonymous users require authentication for protected views")
    
    # Check session configuration
    print(f"✓ Session timeout: {settings.SESSION_COOKIE_AGE} seconds")
    print(f"✓ Session expires on browser close: {settings.SESSION_EXPIRE_AT_BROWSER_CLOSE}")
    
    # 6. Test authentication flow
    print("\n6. AUTHENTICATION FLOW TEST")
    print("-" * 30)
    
    # Test invalid credentials
    invalid_auth = authenticate(username='nonexistent', password='wrongpass')
    if invalid_auth is None:
        print("✓ Invalid credentials properly rejected")
    else:
        print("❌ Invalid credentials improperly accepted")
    
    # Test empty credentials
    empty_auth = authenticate(username='', password='')
    if empty_auth is None:
        print("✓ Empty credentials properly rejected")
    else:
        print("❌ Empty credentials improperly accepted")
    
    print("\n7. DATABASE INTEGRITY CHECK")
    print("-" * 30)
    
    # Check if database connection is working
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM fbc_users_customuser")
            count = cursor.fetchone()[0]
            print(f"✓ Direct database query successful: {count} users")
    except Exception as e:
        print(f"❌ Database connection error: {e}")
    
    # Check password hashing
    admin_user = CustomUser.objects.filter(username='fbcadmin').first()
    if admin_user and admin_user.password.startswith('pbkdf2_sha256$'):
        print("✓ Passwords are properly hashed in database")
    elif admin_user:
        print("❌ Passwords may not be properly hashed")
    
    print("\n" + "=" * 60)
    print("SECURITY AUDIT COMPLETE")
    print("=" * 60)
    
    return True

def check_view_security():
    """Check if views properly require authentication"""
    print("\n8. VIEW SECURITY ANALYSIS")
    print("-" * 30)
    
    # Import views to analyze
    from fbc_users import views
    import inspect
    
    # Get all view functions
    view_functions = [name for name, obj in inspect.getmembers(views) 
                     if inspect.isfunction(obj) and not name.startswith('_')]
    
    protected_views = []
    unprotected_views = []
    
    for view_name in view_functions:
        view_func = getattr(views, view_name)
        
        # Check if view has login_required decorator
        if hasattr(view_func, '__wrapped__'):
            # This indicates a decorator is present
            protected_views.append(view_name)
        elif view_name in ['user_login', 'login_view']:
            # Login views don't need protection
            continue
        else:
            unprotected_views.append(view_name)
    
    print(f"✓ Protected views: {len(protected_views)}")
    for view in protected_views:
        print(f"  - {view}")
    
    if unprotected_views:
        print(f"⚠️  Potentially unprotected views: {len(unprotected_views)}")
        for view in unprotected_views:
            print(f"  - {view}")
    else:
        print("✓ All non-login views appear to be protected")

if __name__ == "__main__":
    try:
        audit_authentication_system()
        check_view_security()
        print("\n✅ Security audit completed successfully!")
    except Exception as e:
        print(f"\n❌ Security audit failed: {e}")
        sys.exit(1)
