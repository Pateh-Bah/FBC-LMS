#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_users.models import CustomUser
from fbc_books.models import Book
from fbc_fines.models import Fine
from decimal import Decimal

def test_fine_creation():
    print("Testing fine creation...")
    
    # Get a test user
    user = CustomUser.objects.first()
    if not user:
        print("No users found!")
        return
    print(f"Test user: {user.username}")
    
    # Get a test book
    book = Book.objects.first()
    print(f"Test book: {book.title if book else 'No books found'}")
    
    # Check existing fines
    existing_fines = Fine.objects.count()
    print(f"Existing fines in database: {existing_fines}")
    
    # Create a test fine
    try:
        fine = Fine.objects.create(
            user=user,
            book=book,
            fine_type='general',
            amount=Decimal('25.00'),
            reason='Test fine created via script'
        )
        print(f"✅ Successfully created fine: {fine}")
        print(f"   - Fine ID: {fine.id}")
        print(f"   - Amount: Le {fine.amount}")
        print(f"   - Type: {fine.get_fine_type_display()}")
        print(f"   - Status: {fine.status}")
        print(f"   - Date: {fine.date_issued}")
        
        # Check if fine appears in queries
        total_fines = Fine.objects.count()
        print(f"Total fines now: {total_fines}")
        
        # List all fines
        print("\nAll fines in database:")
        for f in Fine.objects.all():
            print(f"  - {f.id}: {f.user.username} - Le {f.amount} ({f.status}) - {f.fine_type}")
            
    except Exception as e:
        print(f"❌ Error creating fine: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fine_creation()
