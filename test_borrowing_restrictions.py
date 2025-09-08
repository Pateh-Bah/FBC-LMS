#!/usr/bin/env python
"""
Test script to verify the borrowing restrictions implementation
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse
from fbc_books.models import Book, BookBorrowing, Category, Author
from fbc_users.models import CustomUser
from datetime import date, timedelta

class BorrowingRestrictionsTest:
    def __init__(self):
        self.client = Client()
        self.User = get_user_model()
        
    def setUp(self):
        """Set up test data"""
        print("Setting up test data...")
        
        # Create test category and author
        self.category = Category.objects.get_or_create(name="Test Category")[0]
        self.author = Author.objects.get_or_create(name="Test Author")[0]
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            isbn="1234567890123",
            publication_year=2023,
            status='available',
            book_type='physical',
            available_copies=1,
            category=self.category
        )
        self.book1.authors.add(self.author)
        
        self.book2 = Book.objects.create(
            title="Test Book 2",
            isbn="1234567890124",
            publication_year=2023,
            status='available',
            book_type='physical',
            available_copies=1,
            category=self.category
        )
        self.book2.authors.add(self.author)
        
        self.book3 = Book.objects.create(
            title="Test Book 3",
            isbn="1234567890125",
            publication_year=2023,
            status='available',
            book_type='physical',
            available_copies=1,
            category=self.category
        )
        self.book3.authors.add(self.author)
        
        # Create test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            user_type='student'
        )
        
    def cleanup(self):
        """Clean up test data"""
        print("Cleaning up test data...")
        # Delete test borrowings
        BookBorrowing.objects.filter(user=self.user).delete()
        # Delete test books
        Book.objects.filter(title__startswith="Test Book").delete()
        # Delete test user
        CustomUser.objects.filter(username='testuser').delete()
        
    def test_normal_borrowing(self):
        """Test that normal borrowing works"""
        print("\n1. Testing normal borrowing...")
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Check book detail page context
        response = self.client.get(reverse('fbc_books:book_detail', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['can_borrow'])
        self.assertEqual(response.context['borrow_restriction_message'], "")
        print("✓ Book detail page shows borrowing is allowed")
        
        # Borrow the book
        response = self.client.post(reverse('fbc_books:borrow_book', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful borrowing
        
        # Check that borrowing was created
        borrowing = BookBorrowing.objects.filter(user=self.user, book=self.book1, status='active').first()
        self.assertIsNotNone(borrowing)
        print("✓ Book successfully borrowed")
        
    def test_duplicate_borrowing_restriction(self):
        """Test that users cannot borrow the same book twice"""
        print("\n2. Testing duplicate borrowing restriction...")
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Borrow the book first time
        response = self.client.post(reverse('fbc_books:borrow_book', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 302)
        print("✓ First borrowing successful")
        
        # Check book detail page context after borrowing
        response = self.client.get(reverse('fbc_books:book_detail', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['can_borrow'])
        self.assertEqual(response.context['borrow_restriction_message'], "You have already borrowed this book.")
        print("✓ Book detail page shows duplicate borrowing restriction")
        
        # Try to borrow the same book again
        response = self.client.post(reverse('fbc_books:borrow_book', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect with error message
        
        # Check that no new borrowing was created
        borrowings_count = BookBorrowing.objects.filter(user=self.user, book=self.book1, status='active').count()
        self.assertEqual(borrowings_count, 1)
        print("✓ Duplicate borrowing prevented")
        
    def test_max_borrowing_limit(self):
        """Test that users cannot borrow more than 2 books"""
        print("\n3. Testing maximum borrowing limit...")
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Borrow first book
        response = self.client.post(reverse('fbc_books:borrow_book', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 302)
        print("✓ First book borrowed")
        
        # Borrow second book
        response = self.client.post(reverse('fbc_books:borrow_book', args=[self.book2.pk]))
        self.assertEqual(response.status_code, 302)
        print("✓ Second book borrowed")
        
        # Check book detail page context for third book
        response = self.client.get(reverse('fbc_books:book_detail', args=[self.book3.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['can_borrow'])
        self.assertEqual(response.context['borrow_restriction_message'], "You have reached the maximum borrowing limit of 2 books.")
        print("✓ Book detail page shows borrowing limit restriction")
        
        # Try to borrow third book
        response = self.client.post(reverse('fbc_books:borrow_book', args=[self.book3.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect with error message
        
        # Check that no borrowing was created for third book
        borrowing_exists = BookBorrowing.objects.filter(user=self.user, book=self.book3, status='active').exists()
        self.assertFalse(borrowing_exists)
        print("✓ Third borrowing prevented due to limit")
        
        # Check total active borrowings
        active_borrowings = BookBorrowing.objects.filter(user=self.user, status='active').count()
        self.assertEqual(active_borrowings, 2)
        print("✓ User has exactly 2 active borrowings")
        
    def test_borrowing_after_return(self):
        """Test that borrowing works again after returning a book"""
        print("\n4. Testing borrowing after return...")
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Borrow two books to reach limit
        self.client.post(reverse('fbc_books:borrow_book', args=[self.book1.pk]))
        self.client.post(reverse('fbc_books:borrow_book', args=[self.book2.pk]))
        print("✓ Borrowed 2 books to reach limit")
        
        # Return one book
        borrowing = BookBorrowing.objects.filter(user=self.user, book=self.book1, status='active').first()
        borrowing.status = 'returned'
        borrowing.returned_date = date.today()
        borrowing.save()
        print("✓ Returned one book")
        
        # Check that we can now borrow another book
        response = self.client.get(reverse('fbc_books:book_detail', args=[self.book3.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['can_borrow'])
        self.assertEqual(response.context['borrow_restriction_message'], "")
        print("✓ Can borrow again after return")
        
        # Borrow the third book
        response = self.client.post(reverse('fbc_books:borrow_book', args=[self.book3.pk]))
        self.assertEqual(response.status_code, 302)
        
        # Check that borrowing was successful
        borrowing_exists = BookBorrowing.objects.filter(user=self.user, book=self.book3, status='active').exists()
        self.assertTrue(borrowing_exists)
        print("✓ Third book borrowed successfully after return")
        
    def assertEqual(self, first, second, msg=None):
        """Custom assertion method"""
        if first != second:
            raise AssertionError(f"Expected {first} == {second}")
            
    def assertTrue(self, expr, msg=None):
        """Custom assertion method"""
        if not expr:
            raise AssertionError(f"Expected {expr} to be True")
            
    def assertFalse(self, expr, msg=None):
        """Custom assertion method"""
        if expr:
            raise AssertionError(f"Expected {expr} to be False")
            
    def assertIsNotNone(self, expr, msg=None):
        """Custom assertion method"""
        if expr is None:
            raise AssertionError("Expected value to not be None")
    
    def run_all_tests(self):
        """Run all tests"""
        print("Starting Borrowing Restrictions Tests")
        print("=" * 50)
        
        try:
            self.setUp()
            
            self.test_normal_borrowing()
            self.cleanup()
            
            self.setUp()
            self.test_duplicate_borrowing_restriction()
            self.cleanup()
            
            self.setUp()
            self.test_max_borrowing_limit()
            self.cleanup()
            
            self.setUp()
            self.test_borrowing_after_return()
            self.cleanup()
            
            print("\n" + "=" * 50)
            print("✅ All borrowing restriction tests passed!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            self.cleanup()
            raise

if __name__ == "__main__":
    test_runner = BorrowingRestrictionsTest()
    test_runner.run_all_tests()
