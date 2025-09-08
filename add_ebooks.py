#!/usr/bin/env python
"""
Script to download and add sample ebooks to the FBC Library System
Downloads public domain books from Project Gutenberg
"""

import os
import sys
import django
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_books.models import Book, Category, Author

def download_file(url, filename):
    """Download a file from URL and save it"""
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error downloading {filename}: {e}")
        return None

def create_ebook(title, isbn, author_name, category_name, description, pdf_url):
    """Create an ebook entry in the database"""
    try:
        # Get or create category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'description': f'Books in the {category_name} category'}
        )
        if created:
            print(f"Created category: {category_name}")

        # Get or create author
        author, created = Author.objects.get_or_create(
            name=author_name,
            defaults={'bio': f'Author of {title}'}
        )
        if created:
            print(f"Created author: {author_name}")

        # Check if book already exists
        if Book.objects.filter(isbn=isbn).exists():
            print(f"Book with ISBN {isbn} already exists. Skipping...")
            return None

        # Download PDF content
        pdf_content = download_file(pdf_url, f"{title}.pdf")
        if not pdf_content:
            print(f"Failed to download PDF for {title}")
            return None

        # Create book
        book = Book.objects.create(
            title=title,
            isbn=isbn,
            category=category,
            description=description,
            book_type='ebook',
            total_copies=1,
            available_copies=1,
            status='available'
        )

        # Add author
        book.authors.add(author)

        # Save PDF file
        filename = f"{title.replace(' ', '_').replace(':', '').replace(',', '')}.pdf"
        book.pdf_file.save(filename, ContentFile(pdf_content), save=True)

        print(f"Successfully created ebook: {title}")
        return book

    except Exception as e:
        print(f"Error creating ebook {title}: {e}")
        return None

def main():
    """Main function to add sample ebooks"""
    print("Adding sample ebooks to FBC Library System...")
    print("=" * 50)

    # Sample ebooks from Project Gutenberg (public domain)
    ebooks = [
        {
            'title': 'Pride and Prejudice',
            'isbn': '9781234567890',
            'author': 'Jane Austen',
            'category': 'Classic Literature',
            'description': 'A romantic novel of manners written by Jane Austen in 1813. It follows the character development of Elizabeth Bennet, the dynamic protagonist, who learns about the repercussions of hasty judgments.',
            'pdf_url': 'https://www.gutenberg.org/files/1342/1342-pdf.pdf'
        },
        {
            'title': 'The Adventures of Sherlock Holmes',
            'isbn': '9781234567891',
            'author': 'Arthur Conan Doyle',
            'category': 'Mystery',
            'description': 'A collection of twelve short stories featuring the famous detective Sherlock Holmes, written by Arthur Conan Doyle and published in 1892.',
            'pdf_url': 'https://www.gutenberg.org/files/1661/1661-pdf.pdf'
        },
        {
            'title': 'Alice\'s Adventures in Wonderland',
            'isbn': '9781234567892',
            'author': 'Lewis Carroll',
            'category': 'Children\'s Literature',
            'description': 'A novel written by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll. It tells of a young girl named Alice who falls down a rabbit hole.',
            'pdf_url': 'https://www.gutenberg.org/files/11/11-pdf.pdf'
        },
        {
            'title': 'The Time Machine',
            'isbn': '9781234567893',
            'author': 'H.G. Wells',
            'category': 'Science Fiction',
            'description': 'A science fiction novella by H. G. Wells, published in 1895. The work is generally credited with the popularization of the concept of time travel.',
            'pdf_url': 'https://www.gutenberg.org/files/35/35-pdf.pdf'
        }
    ]

    success_count = 0
    for ebook_data in ebooks:
        print(f"\nProcessing: {ebook_data['title']}")
        book = create_ebook(
            title=ebook_data['title'],
            isbn=ebook_data['isbn'],
            author_name=ebook_data['author'],
            category_name=ebook_data['category'],
            description=ebook_data['description'],
            pdf_url=ebook_data['pdf_url']
        )
        if book:
            success_count += 1

    print("\n" + "=" * 50)
    print(f"Successfully added {success_count} out of {len(ebooks)} ebooks!")
    
    # Display current ebook count
    total_ebooks = Book.objects.filter(book_type='ebook').count()
    print(f"Total ebooks in system: {total_ebooks}")
    print("Done!")

if __name__ == '__main__':
    main()
