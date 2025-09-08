#!/usr/bin/env python
"""
Test script to verify admin dashboard access and URL patterns
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.contrib.auth import authenticate
from django.test import Client, RequestFactory
from django.contrib.auth.models import User

def test_admin_authentication():
    """Test that admin users can authenticate"""
    print("=" * 60)
    print("TESTING ADMIN AUTHENTICATION")
    print("=" * 60)
    
    # Test fbcadmin authentication
    admin_user = authenticate(username='fbcadmin', password='admin123')
    if admin_user:
        print(f"✓ fbcadmin authenticated successfully: {admin_user}")
        print(f"  - Is staff: {admin_user.is_staff}")
        print(f"  - Is superuser: {admin_user.is_superuser}")
        print(f"  - Is active: {admin_user.is_active}")
    else:
        print("✗ fbcadmin authentication failed")
    
    print()

def test_url_patterns():
    """Test that all required URL patterns exist"""
    print("=" * 60)
    print("TESTING URL PATTERNS")
    print("=" * 60)
    
    urls_to_test = [
        ('fbc_books:admin_dashboard', 'Admin Dashboard'),
        ('fbc_books:book_list', 'Book List'),
        ('fbc_payments:payment_history', 'Payment History'),
        ('fbc_fines:manage_fines', 'Manage Fines'),
        ('fbc_users:login', 'Login'),
        ('fbc_users:admin_dashboard', 'User Admin Dashboard'),
    ]
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✓ {description}: {url}")
        except NoReverseMatch as e:
            print(f"✗ {description}: NoReverseMatch - {e}")
    
    print()

def test_admin_dashboard_access():
    """Test admin dashboard access via HTTP client"""
    print("=" * 60)
    print("TESTING ADMIN DASHBOARD ACCESS")
    print("=" * 60)
    
    client = Client()
    
    # First login
    login_response = client.post('/users/login/', {
        'username': 'fbcadmin',
        'password': 'admin123'
    })
    
    print(f"Login response status: {login_response.status_code}")
    if hasattr(login_response, 'url'):
        print(f"Login redirect URL: {login_response.url}")
    
    # Try to access admin dashboard
    try:
        admin_dashboard_url = reverse('fbc_books:admin_dashboard')
        dashboard_response = client.get(admin_dashboard_url)
        print(f"Admin dashboard response status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✓ Admin dashboard accessible")
            # Check if payment_history link would work
            try:
                payment_history_url = reverse('fbc_payments:payment_history')
                print(f"✓ Payment history URL resolved: {payment_history_url}")
            except NoReverseMatch as e:
                print(f"✗ Payment history URL failed: {e}")
        else:
            print(f"✗ Admin dashboard not accessible: {dashboard_response.status_code}")
            
    except Exception as e:
        print(f"✗ Error accessing admin dashboard: {e}")
    
    print()

def test_database_users():
    """Test that required users exist in database"""
    print("=" * 60)
    print("TESTING DATABASE USERS")
    print("=" * 60)
    
    users_to_check = ['fbcadmin', 'fbcstaff']
    
    for username in users_to_check:
        try:
            user = User.objects.get(username=username)
            print(f"✓ User '{username}' exists in database")
            print(f"  - Email: {user.email}")
            print(f"  - First name: {user.first_name}")
            print(f"  - Last name: {user.last_name}")
            print(f"  - Is staff: {user.is_staff}")
            print(f"  - Is superuser: {user.is_superuser}")
            print(f"  - Is active: {user.is_active}")
            print(f"  - Date joined: {user.date_joined}")
        except User.DoesNotExist:
            print(f"✗ User '{username}' not found in database")
        print()

if __name__ == '__main__':
    try:
        test_database_users()
        test_admin_authentication()
        test_url_patterns()
        test_admin_dashboard_access()
        
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("All authentication and URL pattern tests completed.")
        print("If you see any ✗ marks above, those issues need to be addressed.")
        print("If all tests show ✓, the admin dashboard should work correctly.")
        
    except Exception as e:
        print(f"Error running tests: {e}")
        import traceback
        traceback.print_exc()
