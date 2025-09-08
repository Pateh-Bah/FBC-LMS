#!/usr/bin/env python
"""
Check admin user details
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_users.models import CustomUser

def check_admin_user():
    try:
        user = CustomUser.objects.get(username='hawa')
        print(f"User found: {user.username}")
        print(f"Email: {user.email}")
        print(f"First name: {user.first_name}")
        print(f"Last name: {user.last_name}")
        print(f"User type: {user.user_type}")
        print(f"Is staff: {user.is_staff}")
        print(f"Is superuser: {user.is_superuser}")
        print(f"Is active: {user.is_active}")
        print(f"Is suspended: {user.is_suspended}")
        
        # Check if user is considered admin by our function
        from fbc_books.views import is_admin
        print(f"Is admin (our function): {is_admin(user)}")
        
    except CustomUser.DoesNotExist:
        print("User 'hawa' does not exist")
        
    # List all admin users
    print("\nAll admin users:")
    admin_users = CustomUser.objects.filter(user_type='admin')
    for user in admin_users:
        print(f"- {user.username} ({user.email}) - {user.user_type}")
        
    # List all superusers
    print("\nAll superusers:")
    superusers = CustomUser.objects.filter(is_superuser=True)
    for user in superusers:
        print(f"- {user.username} ({user.email}) - {user.user_type}")

if __name__ == "__main__":
    check_admin_user()
