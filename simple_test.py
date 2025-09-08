#!/usr/bin/env python
"""
Simple test to verify template configuration
"""

import os

def test_templates():
    """Test that all admin templates exist and are properly configured."""
    
    admin_templates = [
        'templates/admin/admin_base.html',
        'templates/books/manage_books.html',
        'templates/books/manage_borrowings.html',
        'templates/books/manage_users.html',
        'templates/books/admin_dashboard.html',
        'templates/users/admin_dashboard.html',
        'templates/fbc_fines/manage_fines.html',
        'templates/fbc_notifications/manage_notifications.html',
    ]
    
    print("Testing admin templates...")
    for template in admin_templates:
        if os.path.exists(template):
            print(f"✓ {template} exists")
            
            # Check if it extends the correct base template
            with open(template, 'r', encoding='utf-8') as f:
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
        'templates/books/user_dashboard.html',
        'templates/users/lecturer_dashboard.html',
    ]
    
    for template in user_templates:
        if os.path.exists(template):
            print(f"✓ {template} exists")
            
            # Check if it extends the correct base template
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'base.html' in content or 'user_dashboard_base.html' in content:
                    print(f"  ✓ Uses user base template")
                else:
                    print(f"  ⚠️ Template inheritance unclear")
        else:
            print(f"✗ {template} missing")

if __name__ == "__main__":
    print("FBC Library System - Template Test")
    print("=" * 50)
    
    test_templates()
    
    print("\n" + "=" * 50)
    print("Template test completed!")
