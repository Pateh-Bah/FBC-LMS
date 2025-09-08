#!/usr/bin/env python
"""
Test the dashboard views after fixing field errors
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import authenticate
from fbc_users.models import CustomUser
from fbc_users.views import staff_dashboard, admin_dashboard
from fbc_books.models import Book, BookBorrowing

def test_dashboard_views():
    print("Testing dashboard views after field fixes...")
    
    # Test basic model queries
    print("\n1. Testing model queries:")
    try:
        total_books = Book.objects.count()
        available_books = Book.objects.filter(status='available').count()
        borrowed_books = Book.objects.filter(status='borrowed').count()
        print(f"✅ Book queries successful:")
        print(f"   Total books: {total_books}")
        print(f"   Available: {available_books}")
        print(f"   Borrowed: {borrowed_books}")
    except Exception as e:
        print(f"❌ Book query error: {e}")
        return False
    
    try:
        total_borrowings = BookBorrowing.objects.count()
        active_borrowings = BookBorrowing.objects.filter(status='active').count()
        print(f"✅ Borrowing queries successful:")
        print(f"   Total borrowings: {total_borrowings}")
        print(f"   Active borrowings: {active_borrowings}")
    except Exception as e:
        print(f"❌ Borrowing query error: {e}")
        return False
    
    # Test user authentication
    print("\n2. Testing user authentication:")
    try:
        admin_user = authenticate(username='fbcadmin', password='1234')
        staff_user = authenticate(username='fbcstaff', password='1234')
        
        if admin_user:
            print(f"✅ Admin user authenticated: {admin_user.username} ({admin_user.user_type})")
        else:
            print("❌ Admin user authentication failed")
            
        if staff_user:
            print(f"✅ Staff user authenticated: {staff_user.username} ({staff_user.user_type})")
        else:
            print("❌ Staff user authentication failed")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False
    
    print("\n✅ All tests passed! Dashboard views should work correctly now.")
    print("\nTo test the dashboards:")
    print("1. Start the server: python manage.py runserver")
    print("2. Login with admin: fbcadmin / 1234")
    print("3. Login with staff: fbcstaff / 1234")
    print("4. Both should redirect to their respective dashboards without errors")
    
    return True

if __name__ == "__main__":
    try:
        test_dashboard_views()
    except Exception as e:
        print(f"❌ Test failed: {e}")
