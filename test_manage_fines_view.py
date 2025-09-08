#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from fbc_fines.models import Fine
from fbc_books.models import Book
from decimal import Decimal

def test_manage_fines_view():
    print("Testing manage fines view functionality...")
    
    User = get_user_model()
    client = Client()
    
    # Get a staff user for testing
    staff_user = User.objects.filter(is_staff=True).first()
    if not staff_user:
        # Create a staff user
        staff_user = User.objects.create_user(
            username='teststaff',
            email='teststaff@example.com',
            password='testpass123',
            is_staff=True
        )
        print("Created test staff user")
    
    # Login as staff
    client.force_login(staff_user)
    print(f"Logged in as: {staff_user.username}")
    
    # Test GET request to manage fines page
    try:
        url = reverse('fbc_fines:manage_fines')
        response = client.get(url)
        print(f"GET request status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Manage fines page loads successfully")
            
            # Check if fines are in context
            fines = response.context.get('fines')
            if fines:
                print(f"✅ Found {len(fines)} fines in context")
                for fine in fines:
                    print(f"   - Fine {fine.id}: {fine.user.username} - Le {fine.amount}")
            else:
                print("❌ No fines found in context")
                
            # Check if users and books are in context for the form
            users = response.context.get('users')
            books = response.context.get('books')
            print(f"✅ Found {len(users) if users else 0} users for dropdown")
            print(f"✅ Found {len(books) if books else 0} books for dropdown")
            
        else:
            print(f"❌ GET request failed: {response.status_code}")
            print(response.content.decode()[:500])
            
    except Exception as e:
        print(f"❌ Error testing GET request: {e}")
        import traceback
        traceback.print_exc()
    
    # Test POST request to add new fine
    try:
        test_user = User.objects.exclude(id=staff_user.id).first()
        test_book = Book.objects.first()
        
        if test_user:
            post_data = {
                'user': test_user.id,
                'book': test_book.id if test_book else '',
                'fine_type': 'general',
                'amount': '25.00',
                'reason': 'Test fine via POST request'
            }
            
            # Count fines before
            initial_count = Fine.objects.count()
            
            response = client.post(url, post_data)
            print(f"POST request status: {response.status_code}")
            
            # Count fines after
            final_count = Fine.objects.count()
            
            if final_count > initial_count:
                print("✅ Fine created successfully via POST")
                new_fine = Fine.objects.latest('date_issued')
                print(f"   - New fine: {new_fine.user.username} - Le {new_fine.amount}")
            else:
                print("❌ Fine was not created")
                
        else:
            print("❌ No test user found for POST test")
            
    except Exception as e:
        print(f"❌ Error testing POST request: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n📊 Current fines in database:")
    for fine in Fine.objects.all():
        print(f"   {fine.id}: {fine.user.username} - Le {fine.amount} ({fine.fine_type}) - {fine.status}")

if __name__ == "__main__":
    test_manage_fines_view()
