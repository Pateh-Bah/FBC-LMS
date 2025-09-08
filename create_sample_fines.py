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

def create_sample_fines():
    print("Creating sample fines for testing...")
    
    users = CustomUser.objects.all()[:3]  # Get first 3 users
    books = Book.objects.all()[:3]        # Get first 3 books
    
    if not users:
        print("No users found!")
        return
    
    # Create various types of fines
    sample_fines = [
        {
            'user': users[0],
            'book': books[0] if books else None,
            'fine_type': 'overdue',
            'amount': Decimal('15.00'),
            'reason': 'Book returned 3 days late'
        },
        {
            'user': users[1] if len(users) > 1 else users[0],
            'book': books[1] if len(books) > 1 else books[0] if books else None,
            'fine_type': 'damage',
            'amount': Decimal('50.00'),
            'reason': 'Coffee stain on page 45'
        },
        {
            'user': users[2] if len(users) > 2 else users[0],
            'book': None,  # General fine without book
            'fine_type': 'general',
            'amount': Decimal('10.00'),
            'reason': 'Noise in library'
        },
        {
            'user': users[0],
            'book': books[2] if len(books) > 2 else books[0] if books else None,
            'fine_type': 'lost',
            'amount': Decimal('100.00'),
            'reason': 'Book reported as lost'
        }
    ]
    
    created_fines = []
    for i, fine_data in enumerate(sample_fines, 1):
        try:
            fine = Fine.objects.create(**fine_data)
            created_fines.append(fine)
            print(f"✅ Created fine {i}: {fine.user.username} - Le {fine.amount} ({fine.fine_type})")
        except Exception as e:
            print(f"❌ Error creating fine {i}: {e}")
    
    print(f"\n📊 Total fines in database: {Fine.objects.count()}")
    
    # Show statistics
    from django.db.models import Sum
    total_pending = Fine.objects.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Fine.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    
    print(f"💰 Total outstanding: Le {total_pending}")
    print(f"✅ Total collected: Le {total_paid}")
    
    # Mark one fine as paid for demo
    if created_fines:
        first_fine = created_fines[0]
        first_fine.status = 'paid'
        first_fine.save()
        print(f"✅ Marked fine {first_fine.id} as paid for demo")
    
    print("\nSample fines created successfully! 🎉")
    print("You can now test the CRUD operations in the web interface.")

if __name__ == "__main__":
    create_sample_fines()
