import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_books.models import Book, Author, Category

# Create new categories for Sierra Leonean literature
categories = [
    {'name': 'Sierra Leonean Literature', 'description': 'Books by Sierra Leonean authors and about Sierra Leone'},
    {'name': 'African Studies', 'description': 'Books about African history, culture, and society'}
]

category_objects = {}
for cat in categories:
    category_objects[cat['name']], _ = Category.objects.get_or_create(
        name=cat['name'],
        defaults={'description': cat['description']}
    )

# Create Sierra Leonean authors
authors = [
    {'name': 'Aminatta Forna', 'bio': 'Sierra Leonean-Scottish writer, known for her novels about Sierra Leone'},
    {'name': 'Syl Cheney-Coker', 'bio': 'Sierra Leonean poet, novelist, and journalist'},
    {'name': 'Ishmael Beah', 'bio': 'Sierra Leonean author and human rights activist'},
    {'name': 'Yulisa Amadu Maddy', 'bio': 'Sierra Leonean novelist, playwright and dancer'},
    {'name': 'Davidson Nicol', 'bio': 'Sierra Leonean academic, physician, and writer'}
]

author_objects = {}
for auth in authors:
    author_objects[auth['name']], _ = Author.objects.get_or_create(
        name=auth['name'],
        defaults={'bio': auth['bio']}
    )

# Create Sierra Leonean books
books = [
    {
        'title': 'The Memory of Love',
        'isbn': '9780802119650',
        'authors': ['Aminatta Forna'],
        'category': 'Sierra Leonean Literature',
        'description': 'Set in Sierra Leone, this novel interweaves the stories of a British psychologist, a local surgeon, and a former university professor, exploring love, loss, and the legacy of war.',
        'total_copies': 4,
        'available_copies': 4,
        'book_type': 'physical'
    },
    {
        'title': 'A Long Way Gone: Memoirs of a Boy Soldier',
        'isbn': '9780374531263',
        'authors': ['Ishmael Beah'],
        'category': 'Sierra Leonean Literature',
        'description': 'A memoir of Beah\'s time as a child soldier in Sierra Leone and his journey to rehabilitation.',
        'total_copies': 5,
        'available_copies': 5,
        'book_type': 'physical'
    },
    {
        'title': 'The Last Harmattan of Alusine Dunbar',
        'isbn': '9780435905408',
        'authors': ['Syl Cheney-Coker'],
        'category': 'Sierra Leonean Literature',
        'description': 'A magical realist novel that chronicles two centuries of Sierra Leone\'s history.',
        'total_copies': 3,
        'available_copies': 3,
        'book_type': 'physical'
    },
    {
        'title': 'No Past, No Present, No Future',
        'isbn': '9780435900924',
        'authors': ['Yulisa Amadu Maddy'],
        'category': 'Sierra Leonean Literature',
        'description': 'A novel about three young Sierra Leoneans and their experiences in post-independence Africa.',
        'total_copies': 3,
        'available_copies': 3,
        'book_type': 'physical'
    },
    {
        'title': 'Two African Tales',
        'isbn': '9789988550226',
        'authors': ['Davidson Nicol'],
        'category': 'Sierra Leonean Literature',
        'description': 'A collection of short stories exploring Sierra Leonean culture and society.',
        'total_copies': 2,
        'available_copies': 2,
        'book_type': 'physical'
    },
    {
        'title': 'The Devil that Danced on the Water',
        'isbn': '9780802140487',
        'authors': ['Aminatta Forna'],
        'category': 'African Studies',
        'description': 'A memoir about the author\'s father, a Sierra Leonean politician, and the country\'s political history.',
        'total_copies': 3,
        'available_copies': 3,
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
