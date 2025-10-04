#!/usr/bin/env python
"""
Test script to verify PDF e-book functionality after fixes
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_books.models import Book
from django.conf import settings

def test_ebook_functionality():
    """Test e-book PDF functionality"""
    print("=== E-Book Functionality Test ===\n")
    
    # Check settings
    print("Django Settings:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"  X_FRAME_OPTIONS: {getattr(settings, 'X_FRAME_OPTIONS', 'Not set')}")
    print()
    
    # Find e-books
    ebooks = Book.objects.filter(book_type='ebook')
    print(f"Found {ebooks.count()} e-books in database:")
    
    for book in ebooks:
        print(f"  - {book.title} (ID: {book.pk})")
        if book.pdf_file:
            print(f"    PDF: {book.pdf_file.name} ({book.pdf_file.url})")
            file_exists = os.path.exists(book.pdf_file.path)
            print(f"    File exists: {file_exists}")
            if file_exists:
                file_size = os.path.getsize(book.pdf_file.path) 
                print(f"    File size: {file_size:,} bytes")
                
                # Show URLs
                print(f"    Preview URL: http://127.0.0.1:8000/books/{book.pk}/preview/")
                print(f"    Reader URL: http://127.0.0.1:8000/books/{book.pk}/read/")
                print(f"    Direct PDF: http://127.0.0.1:8000{book.pdf_file.url}")
        else:
            print("    No PDF file attached")
        print()
    
    print("=== Test Complete ===")
    print("\nInstructions:")
    print("1. Make sure Django development server is running")
    print("2. Visit the preview/reader URLs above")
    print("3. PDFs should now load directly in the browser")

if __name__ == '__main__':
    test_ebook_functionality()
