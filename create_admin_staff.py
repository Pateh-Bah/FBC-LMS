#!/usr/bin/env python
"""
Script to create admin and staff users
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_users.models import CustomUser

def create_users():
    print("Creating admin and staff users...")
    
    # Create admin user
    try:
        admin_user = CustomUser.objects.get(username='fbcadmin')
        print(f"Admin user 'fbcadmin' already exists")
    except CustomUser.DoesNotExist:
        admin_user = CustomUser.objects.create_user(
            username='fbcadmin',
            email='fbcadmin@fbc.com',
            password='1234',
            first_name='FBC',
            last_name='Admin',
            user_type='admin',
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Created admin user: {admin_user.username}")
    
    # Create staff user
    try:
        staff_user = CustomUser.objects.get(username='fbcstaff')
        print(f"Staff user 'fbcstaff' already exists")
    except CustomUser.DoesNotExist:
        staff_user = CustomUser.objects.create_user(
            username='fbcstaff',
            email='fbcstaff@fbc.com',
            password='1234',
            first_name='FBC',
            last_name='Staff',
            user_type='staff',
            is_staff=True,
            is_superuser=False
        )
        print(f"✅ Created staff user: {staff_user.username}")
    
    print("\nUser Summary:")
    print("=" * 40)
    
    # Display admin user details
    admin_user = CustomUser.objects.get(username='fbcadmin')
    print(f"Admin User: {admin_user.username}")
    print(f"  Email: {admin_user.email}")
    print(f"  Name: {admin_user.get_full_name()}")
    print(f"  User Type: {admin_user.user_type}")
    print(f"  Is Staff: {admin_user.is_staff}")
    print(f"  Is Superuser: {admin_user.is_superuser}")
    print(f"  Password: 1234")
    
    print()
    
    # Display staff user details
    staff_user = CustomUser.objects.get(username='fbcstaff')
    print(f"Staff User: {staff_user.username}")
    print(f"  Email: {staff_user.email}")
    print(f"  Name: {staff_user.get_full_name()}")
    print(f"  User Type: {staff_user.user_type}")
    print(f"  Is Staff: {staff_user.is_staff}")
    print(f"  Is Superuser: {staff_user.is_superuser}")
    print(f"  Password: 1234")
    
    print("\n✅ Users created successfully!")
    print("\nLogin Instructions:")
    print("- Admin login: username='fbcadmin', password='1234'")
    print("- Staff login: username='fbcstaff', password='1234'")
    print("- Both users can access Django admin at /admin/")
    print("- Admin user will be redirected to /dashboard/admin/ after custom login")
    print("- Staff user will be redirected to /dashboard/ after custom login")

if __name__ == "__main__":
    create_users()
