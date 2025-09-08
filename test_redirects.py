#!/usr/bin/env python
"""
Test script to check URL redirects
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_redirects():
    print("Testing URL redirects...")
    print("=" * 50)
    
    client = Client()
    
    # Test old admin URLs
    old_urls = [
        '/admin/dashboard/',
        '/admin/manage-books/',
        '/admin/manage-users/',
        '/admin/manage-borrowings/',
    ]
    
    for old_url in old_urls:
        print(f"\nTesting: {old_url}")
        try:
            response = client.get(old_url, follow=False)
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 301:
                print(f"  ✅ Permanent redirect to: {response['Location']}")
            elif response.status_code == 302:
                print(f"  ✅ Redirect to: {response['Location']}")
            elif response.status_code == 404:
                print(f"  ❌ Not Found - redirect not working")
            else:
                print(f"  ⚠️  Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Testing target URLs...")
    
    # Test target URLs
    target_urls = [
        ('fbc_books:admin_dashboard', '/dashboard/admin/'),
        ('fbc_books:manage_books', '/manage/books/'),
        ('fbc_books:manage_users', '/manage/users/'),
        ('fbc_books:manage_borrowings', '/manage/borrowings/'),
    ]
    
    for url_name, expected_path in target_urls:
        try:
            actual_path = reverse(url_name)
            if actual_path == expected_path:
                print(f"✅ {url_name} → {actual_path}")
            else:
                print(f"❌ {url_name} → {actual_path} (expected: {expected_path})")
        except Exception as e:
            print(f"❌ {url_name} → Error: {str(e)}")

if __name__ == "__main__":
    test_redirects()
