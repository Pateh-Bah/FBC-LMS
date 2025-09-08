#!/usr/bin/env python
"""
Check if users are actually in the database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_users.models import CustomUser
from django.contrib.auth import authenticate

def check_database():
    print("Checking SQLite database for users...")
    print("=" * 60)
    
    # Check all users in database
    all_users = CustomUser.objects.all()
    print(f"Total users in database: {all_users.count()}")
    print()
    
    # List all users
    print("All users in database:")
    for user in all_users:
        print(f"- {user.username} | {user.email} | {user.user_type} | Staff: {user.is_staff} | Super: {user.is_superuser}")
    
    print()
    print("=" * 60)
    
    # Specifically check for our target users
    try:
        fbcadmin = CustomUser.objects.get(username='fbcadmin')
        print("✅ fbcadmin found in database:")
        print(f"   ID: {fbcadmin.id}")
        print(f"   Username: {fbcadmin.username}")
        print(f"   Email: {fbcadmin.email}")
        print(f"   User Type: {fbcadmin.user_type}")
        print(f"   Is Staff: {fbcadmin.is_staff}")
        print(f"   Is Superuser: {fbcadmin.is_superuser}")
        print(f"   Password hash: {fbcadmin.password[:50]}...")
        
        # Test authentication
        auth_test = authenticate(username='fbcadmin', password='1234')
        if auth_test:
            print("   ✅ Authentication works")
        else:
            print("   ❌ Authentication failed")
            
    except CustomUser.DoesNotExist:
        print("❌ fbcadmin NOT found in database")
    
    print()
    
    try:
        fbcstaff = CustomUser.objects.get(username='fbcstaff')
        print("✅ fbcstaff found in database:")
        print(f"   ID: {fbcstaff.id}")
        print(f"   Username: {fbcstaff.username}")
        print(f"   Email: {fbcstaff.email}")
        print(f"   User Type: {fbcstaff.user_type}")
        print(f"   Is Staff: {fbcstaff.is_staff}")
        print(f"   Is Superuser: {fbcstaff.is_superuser}")
        print(f"   Password hash: {fbcstaff.password[:50]}...")
        
        # Test authentication
        auth_test = authenticate(username='fbcstaff', password='1234')
        if auth_test:
            print("   ✅ Authentication works")
        else:
            print("   ❌ Authentication failed")
            
    except CustomUser.DoesNotExist:
        print("❌ fbcstaff NOT found in database")

if __name__ == "__main__":
    check_database()
