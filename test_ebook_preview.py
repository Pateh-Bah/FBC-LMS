#!/usr/bin/env python
"""
Test script to verify ebook preview functionality
"""
import os
import sys
import django

# Add the project directory to Python path
project_dir = r"c:\Users\pateh\Downloads\Web\Django\dj fbc vs"
sys.path.insert(0, project_dir)
os.chdir(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_books.models import Book
from django.urls import reverse

print("=== EBOOK PREVIEW FUNCTIONALITY TEST ===")

# Check if there are any ebooks in the database
ebooks = Book.objects.filter(book_type='ebook')
print(f"Found {ebooks.count()} e-books in the database")

if ebooks.exists():
    for book in ebooks[:3]:  # Check first 3 ebooks
        print(f"\n📚 E-book: {book.title}")
        print(f"   ID: {book.pk}")
        print(f"   Authors: {', '.join([a.name for a in book.authors.all()])}")
        print(f"   Has PDF: {'Yes' if book.pdf_file else 'No'}")
        if book.pdf_file:
            print(f"   PDF Path: {book.pdf_file.name}")
        
        # Generate URLs
        try:
            preview_url = reverse('fbc_books:ebook_preview', kwargs={'pk': book.pk})
            reader_url = reverse('fbc_books:ebook_reader', kwargs={'pk': book.pk})
            download_url = reverse('fbc_books:ebook_download', kwargs={'pk': book.pk})
            
            print(f"   📖 Preview URL: http://127.0.0.1:8000{preview_url}")
            print(f"   📱 Reader URL: http://127.0.0.1:8000{reader_url}")  
            print(f"   💾 Download URL: http://127.0.0.1:8000{download_url}")
        except Exception as e:
            print(f"   ❌ URL generation error: {e}")
else:
    print("\n⚠️  No e-books found in database")
    print("To test the preview functionality:")
    print("1. Add an e-book through the admin panel at /books/add/")
    print("2. Select 'E-Book' as the book type")
    print("3. Upload a PDF file")
    print("4. Then visit the preview URL")

print("\n=== TESTING COMPLETE ===")
print("If you have e-books with PDFs, you can test at:")
print("🔗 http://127.0.0.1:8000/books/12/preview/")
print("(Replace '12' with the actual book ID)")
