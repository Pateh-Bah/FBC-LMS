#!/usr/bin/env python
"""
Quick verification that database authentication is working
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth import authenticate
from fbc_users.models import CustomUser

def quick_auth_test():
    print("🔒 FBC Library System - Database Authentication Test")
    print("=" * 55)
    
    # Test 1: Verify users exist in database
    print("\n1. Database User Verification")
    print("-" * 30)
    
    try:
        admin_user = CustomUser.objects.get(username='fbcadmin')
        print(f"✅ Admin user found: {admin_user.username} (Type: {admin_user.user_type})")
    except CustomUser.DoesNotExist:
        print("❌ Admin user NOT found in database")
        return False
    
    try:
        staff_user = CustomUser.objects.get(username='fbcstaff')
        print(f"✅ Staff user found: {staff_user.username} (Type: {staff_user.user_type})")
    except CustomUser.DoesNotExist:
        print("❌ Staff user NOT found in database")
        return False
    
    # Test 2: Authenticate against database
    print("\n2. Database Authentication Test")
    print("-" * 30)
    
    # Test admin authentication
    admin_auth = authenticate(username='fbcadmin', password='1234')
    if admin_auth and admin_auth.id == admin_user.id:
        print("✅ Admin authentication: SUCCESS")
    else:
        print("❌ Admin authentication: FAILED")
        return False
    
    # Test staff authentication
    staff_auth = authenticate(username='fbcstaff', password='1234')
    if staff_auth and staff_auth.id == staff_user.id:
        print("✅ Staff authentication: SUCCESS")
    else:
        print("❌ Staff authentication: FAILED")
        return False
    
    # Test 3: Invalid credentials
    print("\n3. Invalid Credentials Test")
    print("-" * 30)
    
    invalid_auth = authenticate(username='fbcadmin', password='wrongpassword')
    if invalid_auth is None:
        print("✅ Invalid password properly rejected")
    else:
        print("❌ Invalid password improperly accepted")
        return False
    
    nonexistent_auth = authenticate(username='nonexistent', password='1234')
    if nonexistent_auth is None:
        print("✅ Non-existent user properly rejected")
    else:
        print("❌ Non-existent user improperly accepted")
        return False
    
    print("\n4. System Configuration")
    print("-" * 30)
    
    from django.conf import settings
    print(f"✅ Custom User Model: {settings.AUTH_USER_MODEL}")
    print(f"✅ Database Engine: {settings.DATABASES['default']['ENGINE']}")
    
    print("\n" + "=" * 55)
    print("🎉 ALL TESTS PASSED - Database authentication is working correctly!")
    print("✅ All users are verified against the database")
    print("✅ Invalid credentials are properly rejected")
    print("✅ Authentication system is secure and database-backed")
    print("=" * 55)
    
    return True

if __name__ == "__main__":
    try:
        success = quick_auth_test()
        if not success:
            print("\n❌ Some tests failed. Please check the configuration.")
            exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        exit(1)
