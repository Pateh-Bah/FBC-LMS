import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_books.models import Book, Author, Category

# First, create categories
categories = [
    {'name': 'Computer Science', 'description': 'Books related to programming, software development, and computer science'},
    {'name': 'Fiction', 'description': 'Novels and fictional literature'},
    {'name': 'Business', 'description': 'Books about business, management, and entrepreneurship'},
    {'name': 'Science', 'description': 'Books about various scientific disciplines'},
    {'name': 'Mathematics', 'description': 'Books covering mathematical concepts and applications'}
]

category_objects = {}
for cat in categories:
    category_objects[cat['name']], _ = Category.objects.get_or_create(
        name=cat['name'],
        defaults={'description': cat['description']}
    )

# Create authors
authors = [
    {'name': 'Robert C. Martin', 'bio': 'Known as "Uncle Bob", is a software engineer and author'},
    {'name': 'George R.R. Martin', 'bio': 'American novelist and short story writer'},
    {'name': 'Stephen Hawking', 'bio': 'Theoretical physicist and cosmologist'},
    {'name': 'Malcolm Gladwell', 'bio': 'Canadian journalist and author'},
    {'name': 'J.K. Rowling', 'bio': 'British author, best known for the Harry Potter series'}
]

author_objects = {}
for auth in authors:
    author_objects[auth['name']], _ = Author.objects.get_or_create(
        name=auth['name'],
        defaults={'bio': auth['bio']}
    )

# Create books
books = [
    {
        'title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
        'isbn': '9780132350884',
        'authors': ['Robert C. Martin'],
        'category': 'Computer Science',
        'description': 'A book about writing clean, maintainable code',
        'total_copies': 5,
        'available_copies': 5,
        'book_type': 'physical'
    },
    {
        'title': 'A Game of Thrones',
        'isbn': '9780553573404',
        'authors': ['George R.R. Martin'],
        'category': 'Fiction',
        'description': 'The first book in the A Song of Ice and Fire series',
        'total_copies': 3,
        'available_copies': 3,
        'book_type': 'physical'
    },
    {
        'title': 'A Brief History of Time',
        'isbn': '9780553380163',
        'authors': ['Stephen Hawking'],
        'category': 'Science',
        'description': 'A landmark volume in science writing by one of the great minds of our time',
        'total_copies': 4,
        'available_copies': 4,
        'book_type': 'physical'
    },
    {
        'title': 'Outliers: The Story of Success',
        'isbn': '9780316017930',
        'authors': ['Malcolm Gladwell'],
        'category': 'Business',
        'description': 'Explores what makes high-achievers different',
        'total_copies': 3,
        'available_copies': 3,
        'book_type': 'physical'
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'isbn': '9780747532699',
        'authors': ['J.K. Rowling'],
        'category': 'Fiction',
        'description': 'The first book in the Harry Potter series',
        'total_copies': 6,
        'available_copies': 6,
        'book_type': 'physical'
    }
]

# Add books to database
for book_data in books:
    book, created = Book.objects.get_or_create(
        isbn=book_data['isbn'],
        defaults={
            'title': book_data['title'],
            'category': category_objects[book_data['category']],
            'description': book_data['description'],
            'total_copies': book_data['total_copies'],
            'available_copies': book_data['available_copies'],
            'book_type': book_data['book_type'],
            'status': 'available'
        }
    )
    
    if created:
        # Add authors
        for author_name in book_data['authors']:
            book.authors.add(author_objects[author_name])
        print(f'Added book: {book.title}')
    else:
        print(f'Book already exists: {book.title}')
