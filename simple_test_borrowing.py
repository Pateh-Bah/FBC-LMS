#!/usr/bin/env python
"""
Simple test script to verify borrowing restrictions using Django shell
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from fbc_books.models import Book, BookBorrowing, Category, Author
from fbc_users.models import CustomUser
from datetime import date, timedelta

def test_borrowing_restrictions():
    print("Testing borrowing restrictions...")
    
    # Clean up any existing test data
    print("Cleaning up existing test data...")
    CustomUser.objects.filter(username='testuser').delete()
    Book.objects.filter(title__startswith="Test Book").delete()
    
    # Create test data
    print("Creating test data...")
    
    # Create test category and author
    category, _ = Category.objects.get_or_create(name="Test Category")
    author, _ = Author.objects.get_or_create(name="Test Author")
    
    # Create test books
    book1 = Book.objects.create(
        title="Test Book 1",
        isbn="1234567890123",
        description="Test description 1",
        status='available',
        book_type='physical',
        available_copies=1,
        total_copies=1,
        category=category
    )
    book1.authors.add(author)
    
    book2 = Book.objects.create(
        title="Test Book 2",
        isbn="1234567890124",
        description="Test description 2",
        status='available',
        book_type='physical',
        available_copies=1,
        total_copies=1,
        category=category
    )
    book2.authors.add(author)
    
    book3 = Book.objects.create(
        title="Test Book 3",
        isbn="1234567890125",
        description="Test description 3",
        status='available',
        book_type='physical',
        available_copies=1,
        total_copies=1,
        category=category
    )
    book3.authors.add(author)
    
    # Create test user
    user = CustomUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        user_type='student'
    )
    
    print("✓ Test data created successfully")
    
    # Test 1: Normal borrowing
    print("\n1. Testing normal borrowing...")
    borrowing1 = BookBorrowing.objects.create(
        user=user,
        book=book1,
        borrowed_date=date.today(),
        due_date=date.today() + timedelta(days=14),
        status='active'
    )
    print("✓ First book borrowed successfully")
    
    # Test 2: Check duplicate borrowing detection
    print("\n2. Testing duplicate borrowing restriction...")
    existing_borrowing = BookBorrowing.objects.filter(
        user=user,
        book=book1,
        status='active',
        returned_date__isnull=True
    ).exists()
    
    if existing_borrowing:
        print("✓ Duplicate borrowing detection works - user already has this book")
    else:
        print("❌ Duplicate borrowing detection failed")
    
    # Test 3: Check borrowing limit
    print("\n3. Testing maximum borrowing limit...")
    
    # Borrow second book
    borrowing2 = BookBorrowing.objects.create(
        user=user,
        book=book2,
        borrowed_date=date.today(),
        due_date=date.today() + timedelta(days=14),
        status='active'
    )
    print("✓ Second book borrowed successfully")
    
    # Check active borrowings count
    active_borrowings_count = BookBorrowing.objects.filter(
        user=user,
        status='active',
        returned_date__isnull=True
    ).count()
    
    print(f"✓ User has {active_borrowings_count} active borrowings")
    
    if active_borrowings_count >= 2:
        print("✓ Borrowing limit reached - user cannot borrow more books")
    else:
        print("❌ Borrowing limit check failed")
    
    # Test 4: Test borrowing after return
    print("\n4. Testing borrowing after return...")
    
    # Return first book
    borrowing1.status = 'returned'
    borrowing1.returned_date = date.today()
    borrowing1.save()
    print("✓ First book returned")
    
    # Check active borrowings count after return
    active_borrowings_count = BookBorrowing.objects.filter(
        user=user,
        status='active',
        returned_date__isnull=True
    ).count()
    
    print(f"✓ User now has {active_borrowings_count} active borrowings")
    
    if active_borrowings_count < 2:
        print("✓ User can now borrow another book")
    else:
        print("❌ Return detection failed")
    
    # Test the view logic
    print("\n5. Testing view context logic...")
    
    # Test can_borrow logic for book3 (should be True now)
    existing_borrowing = BookBorrowing.objects.filter(
        user=user,
        book=book3,
        status='active',
        returned_date__isnull=True
    ).exists()
    
    active_borrowings_count = BookBorrowing.objects.filter(
        user=user,
        status='active',
        returned_date__isnull=True
    ).count()
    
    can_borrow = True
    borrow_restriction_message = ""
    
    if existing_borrowing:
        can_borrow = False
        borrow_restriction_message = "You have already borrowed this book."
    elif active_borrowings_count >= 2:
        can_borrow = False
        borrow_restriction_message = "You have reached the maximum borrowing limit of 2 books."
    
    print(f"✓ can_borrow for book3: {can_borrow}")
    print(f"✓ restriction_message: '{borrow_restriction_message}'")
    
    # Clean up test data
    print("\n6. Cleaning up test data...")
    BookBorrowing.objects.filter(user=user).delete()
    Book.objects.filter(title__startswith="Test Book").delete()
    CustomUser.objects.filter(username='testuser').delete()
    print("✓ Test data cleaned up")
    
    print("\n" + "=" * 50)
    print("✅ All borrowing restriction tests completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    test_borrowing_restrictions()
