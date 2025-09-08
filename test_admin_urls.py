#!/usr/bin/env python
"""
Test URL patterns and admin dashboard access
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.contrib.auth import authenticate

def test_url_patterns():
    print("🔗 Testing URL patterns for admin/staff dashboards...")
    
    # Test URL patterns that should exist
    url_tests = [
        ('fbc_books:admin_dashboard', 'Admin Dashboard (Books)'),
        ('fbc_users:staff_dashboard', 'Staff Dashboard (Users)'),
        ('fbc_users:admin_dashboard', 'Admin Dashboard (Users)'),
        ('fbc_books:manage_books', 'Manage Books'),
        ('fbc_books:add_book', 'Add Book'),
        ('fbc_fines:manage_fines', 'Manage Fines'),
        ('fbc_payments:payment_history', 'Payment History'),
        ('fbc_payments:my_payments', 'My Payments'),
    ]
    
    print("\n1. URL Pattern Tests:")
    print("-" * 40)
    
    for url_name, description in url_tests:
        try:
            url = reverse(url_name)
            print(f"✅ {description:25} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {description:25} -> URL not found: {url_name}")
    
    # Test authentication and redirection logic
    print("\n2. Authentication Tests:")
    print("-" * 40)
    
    try:
        admin_user = authenticate(username='fbcadmin', password='1234')
        if admin_user:
            print(f"✅ Admin user authenticated: {admin_user.username} ({admin_user.user_type})")
            print(f"   Should redirect to: {reverse('fbc_books:admin_dashboard')}")
        else:
            print("❌ Admin authentication failed")
    except Exception as e:
        print(f"❌ Admin auth error: {e}")
    
    try:
        staff_user = authenticate(username='fbcstaff', password='1234')
        if staff_user:
            print(f"✅ Staff user authenticated: {staff_user.username} ({staff_user.user_type})")
            print(f"   Should redirect to: {reverse('fbc_users:staff_dashboard')}")
        else:
            print("❌ Staff authentication failed")
    except Exception as e:
        print(f"❌ Staff auth error: {e}")
    
    print("\n3. Dashboard Access Summary:")
    print("-" * 40)
    print("📋 ADMIN USERS:")
    print("   - Login URL: /users/login/")
    print("   - Credentials: fbcadmin / 1234")
    print("   - Redirect: /dashboard/admin/ (Books app)")
    print("   - Features: Full system management")
    
    print("\n📋 STAFF USERS:")
    print("   - Login URL: /users/login/")
    print("   - Credentials: fbcstaff / 1234")
    print("   - Redirect: /users/staff-dashboard/ (Users app)")
    print("   - Features: Book/user management, operations")
    
    print("\n📋 DJANGO ADMIN:")
    print("   - Login URL: /admin/")
    print("   - Same credentials work")
    print("   - Features: Database administration")
    
    print("\n✅ URL pattern testing complete!")

if __name__ == "__main__":
    test_url_patterns()
