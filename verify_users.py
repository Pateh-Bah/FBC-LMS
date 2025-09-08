#!/usr/bin/env python
"""
Verify the created admin and staff users
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth import authenticate
from fbc_users.models import CustomUser

def verify_users():
    print("Verifying created users...")
    print("=" * 50)
    
    # Test admin user authentication
    admin_user = authenticate(username='fbcadmin', password='1234')
    if admin_user:
        print("✅ Admin user 'fbcadmin' authentication: SUCCESS")
        print(f"   User Type: {admin_user.user_type}")
        print(f"   Is Staff: {admin_user.is_staff}")
        print(f"   Is Superuser: {admin_user.is_superuser}")
    else:
        print("❌ Admin user 'fbcadmin' authentication: FAILED")
    
    print()
    
    # Test staff user authentication
    staff_user = authenticate(username='fbcstaff', password='1234')
    if staff_user:
        print("✅ Staff user 'fbcstaff' authentication: SUCCESS")
        print(f"   User Type: {staff_user.user_type}")
        print(f"   Is Staff: {staff_user.is_staff}")
        print(f"   Is Superuser: {staff_user.is_superuser}")
    else:
        print("❌ Staff user 'fbcstaff' authentication: FAILED")
    
    print()
    print("Login URLs:")
    print("- Custom Login: http://127.0.0.1:8000/users/login/")
    print("- Django Admin: http://127.0.0.1:8000/admin/")
    print()
    print("Credentials:")
    print("- fbcadmin / 1234 (Admin)")
    print("- fbcstaff / 1234 (Staff)")

if __name__ == "__main__":
    verify_users()
