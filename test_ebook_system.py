#!/usr/bin/env python
"""
Test script to verify PDF e-book functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_books.models import Book
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

def test_ebook_functionality():
    """Test e-book PDF functionality"""
    print("=== E-Book Functionality Test ===\n")
    
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
        else:
            print("    No PDF file attached")
        print()
    
    # Test URLs for book ID 12
    if ebooks.filter(pk=12).exists():
        book = ebooks.get(pk=12)
        print(f"Testing URLs for book: {book.title}")
        
        # Test direct PDF URL
        pdf_url = f"http://127.0.0.1:8000{book.pdf_file.url}"
        print(f"Direct PDF URL: {pdf_url}")
        
        # Test Django URLs
        try:
            preview_url = reverse('fbc_books:ebook_preview', kwargs={'pk': 12})
            reader_url = reverse('fbc_books:ebook_reader', kwargs={'pk': 12}) 
            download_url = reverse('fbc_books:ebook_download', kwargs={'book_id': 12})
            
            print(f"Preview URL: /books{preview_url}")
            print(f"Reader URL: /books{reader_url}")
            print(f"Download URL: /books{download_url}")
            
        except Exception as e:
            print(f"URL reverse error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == '__main__':
    test_ebook_functionality()
