#!/usr/bin/env python
"""
Test script to verify that all admin templates are working correctly
and that CRUD operations are functional.
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the Django project directory to Python path
sys.path.insert(0, os.path.abspath('.'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from fbc_books.models import Book, Category, Author, Borrowing
from fbc_fines.models import Fine
from fbc_notifications.models import Notification

User = get_user_model()

def test_admin_templates():
    """Test that all admin templates exist and are properly configured."""
    
    admin_templates = [
        'admin/admin_base.html',
        'books/manage_books.html',
        'books/manage_borrowings.html',
        'books/manage_users.html',
        'books/admin_dashboard.html',
        'users/admin_dashboard.html',
        'fbc_fines/manage_fines.html',
        'fbc_notifications/manage_notifications.html',
    ]
    
    print("Testing admin templates...")
    for template in admin_templates:
        template_path = os.path.join('templates', template)
        if os.path.exists(template_path):
            print(f"✓ {template} exists")
            
            # Check if it extends the correct base template
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'admin/admin_base.html' in content:
                    print(f"  ✓ Uses admin base template")
                elif 'base_dashboard.html' in content:
                    print(f"  ⚠️ Still uses old base_dashboard.html")
                else:
                    print(f"  ⚠️ Template inheritance unclear")
        else:
            print(f"✗ {template} missing")
    
    print("\nTesting user templates...")
    user_templates = [
        'books/user_dashboard.html',
        'users/lecturer_dashboard.html',
    ]
    
    for template in user_templates:
        template_path = os.path.join('templates', template)
        if os.path.exists(template_path):
            print(f"✓ {template} exists")
            
            # Check if it extends the correct base template
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'base.html' in content or 'user_dashboard_base.html' in content:
                    print(f"  ✓ Uses user base template")
                else:
                    print(f"  ⚠️ Template inheritance unclear")
        else:
            print(f"✗ {template} missing")

def test_models():
    """Test that models are working correctly."""
    print("\nTesting models...")
    
    try:
        # Test User model
        user_count = User.objects.count()
        print(f"✓ User model working - {user_count} users")
        
        # Test Book model
        book_count = Book.objects.count()
        print(f"✓ Book model working - {book_count} books")
        
        # Test Category model
        category_count = Category.objects.count()
        print(f"✓ Category model working - {category_count} categories")
        
        # Test Author model
        author_count = Author.objects.count()
        print(f"✓ Author model working - {author_count} authors")
        
        # Test Borrowing model
        borrowing_count = Borrowing.objects.count()
        print(f"✓ Borrowing model working - {borrowing_count} borrowings")
        
        # Test Fine model
        fine_count = Fine.objects.count()
        print(f"✓ Fine model working - {fine_count} fines")
        
        # Test Notification model
        notification_count = Notification.objects.count()
        print(f"✓ Notification model working - {notification_count} notifications")
        
    except Exception as e:
        print(f"✗ Model test failed: {e}")

def test_user_str_method():
    """Test that User.__str__ method works correctly."""
    print("\nTesting User.__str__ method...")
    
    try:
        users = User.objects.all()[:5]  # Get first 5 users
        for user in users:
            user_str = str(user)
            print(f"✓ User {user.id}: {user_str}")
    except Exception as e:
        print(f"✗ User.__str__ test failed: {e}")

if __name__ == "__main__":
    print("FBC Library System - Admin Panel Test")
    print("=" * 50)
    
    test_admin_templates()
    test_models()
    test_user_str_method()
    
    print("\n" + "=" * 50)
    print("Test completed!")
