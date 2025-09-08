#!/usr/bin/env python
"""
Test authentication after fixing backend issue
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth import authenticate
from fbc_users.models import CustomUser

def test_auth():
    print("Testing authentication after backend fix...")
    
    # Test admin authentication
    admin_user = authenticate(username='fbcadmin', password='1234')
    if admin_user:
        print(f"✅ Admin authentication: SUCCESS")
        print(f"   Backend: {getattr(admin_user, 'backend', 'Not set')}")
        print(f"   User type: {admin_user.user_type}")
    else:
        print("❌ Admin authentication: FAILED")
    
    # Test staff authentication
    staff_user = authenticate(username='fbcstaff', password='1234')
    if staff_user:
        print(f"✅ Staff authentication: SUCCESS") 
        print(f"   Backend: {getattr(staff_user, 'backend', 'Not set')}")
        print(f"   User type: {staff_user.user_type}")
    else:
        print("❌ Staff authentication: FAILED")
    
    print("\nDatabase verification:")
    try:
        admin_db = CustomUser.objects.get(username='fbcadmin')
        staff_db = CustomUser.objects.get(username='fbcstaff')
        print(f"✅ Admin exists in DB: {admin_db.username} ({admin_db.user_type})")
        print(f"✅ Staff exists in DB: {staff_db.username} ({staff_db.user_type})")
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    test_auth()
