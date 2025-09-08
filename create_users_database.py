#!/usr/bin/env python
"""
Django management command to create admin and staff users in database
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_users.models import CustomUser
from django.db import transaction

def create_users_in_database():
    print("Creating users directly in SQLite database...")
    print("=" * 60)
    
    # Use database transaction to ensure data is saved
    with transaction.atomic():
        
        # Check and create fbcadmin
        print("Creating fbcadmin user...")
        try:
            # Delete if exists to recreate
            try:
                existing_admin = CustomUser.objects.get(username='fbcadmin')
                existing_admin.delete()
                print("  - Deleted existing fbcadmin")
            except CustomUser.DoesNotExist:
                pass
            
            # Create new admin user
            admin_user = CustomUser.objects.create_user(
                username='fbcadmin',
                email='fbcadmin@fbc.com',
                password='1234',
                first_name='FBC',
                last_name='Admin',
                user_type='admin',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            # Force save to database
            admin_user.save()
            print(f"  ✅ Created fbcadmin with ID: {admin_user.id}")
            
        except Exception as e:
            print(f"  ❌ Error creating fbcadmin: {str(e)}")
            
        print()
        
        # Check and create fbcstaff
        print("Creating fbcstaff user...")
        try:
            # Delete if exists to recreate
            try:
                existing_staff = CustomUser.objects.get(username='fbcstaff')
                existing_staff.delete()
                print("  - Deleted existing fbcstaff")
            except CustomUser.DoesNotExist:
                pass
            
            # Create new staff user
            staff_user = CustomUser.objects.create_user(
                username='fbcstaff',
                email='fbcstaff@fbc.com',
                password='1234',
                first_name='FBC',
                last_name='Staff',
                user_type='staff',
                is_staff=True,
                is_superuser=False,
                is_active=True
            )
            # Force save to database
            staff_user.save()
            print(f"  ✅ Created fbcstaff with ID: {staff_user.id}")
            
        except Exception as e:
            print(f"  ❌ Error creating fbcstaff: {str(e)}")
    
    print()
    print("=" * 60)
    print("Verifying users in database...")
    
    # Verify users are in database
    all_users = CustomUser.objects.all()
    print(f"Total users in database: {all_users.count()}")
    
    for user in all_users:
        if user.username in ['fbcadmin', 'fbcstaff']:
            print(f"✅ {user.username} in database:")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   User Type: {user.user_type}")
            print(f"   Is Staff: {user.is_staff}")
            print(f"   Is Superuser: {user.is_superuser}")
            print(f"   Is Active: {user.is_active}")
            
            # Test database authentication
            from django.contrib.auth import authenticate
            auth_result = authenticate(username=user.username, password='1234')
            if auth_result:
                print(f"   ✅ Database authentication: SUCCESS")
            else:
                print(f"   ❌ Database authentication: FAILED")
            print()
    
    print("Users successfully created and verified in SQLite database!")
    print("Database file location: db.sqlite3")

if __name__ == "__main__":
    create_users_in_database()
