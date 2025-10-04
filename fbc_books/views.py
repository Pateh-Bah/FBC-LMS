from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import csv
from datetime import timedelta
from .models import Book, Author, Category, BookBorrowing
from fbc_fines.models import Fine
from fbc_notifications.models import LibraryNotification
from django.contrib.auth import get_user_model
from fbc_users.models import CustomUser


# Helper functions for user authentication
def is_admin_or_staff(user):
    return user.is_authenticated and user.user_type in ['admin', 'staff']

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'


def home(request):
    # Get categories for search dropdown
    categories = Category.objects.all()

    # Get recent books (last 6)
    recent_books = (
        Book.objects.select_related("category")
        .prefetch_related("authors")
        .filter(status="available")
        .order_by("-created_at")[:6]
    )

    # Get popular books (top 6 by borrow count)
    popular_books = (
        Book.objects.annotate(borrow_count=Count("borrowings"))
        .select_related("category")
        .prefetch_related("authors")
        .filter(status="available")
        .order_by("-borrow_count")[:6]
    )

    context = {
        "recent_books": recent_books,
        "popular_books": popular_books,
        "categories": categories,
    }
    return render(request, "books/home.html", context)


def book_list(request):
    # Get query parameters
    query = request.GET.get("q", "")
    book_type = request.GET.get("type", "all")
    availability = request.GET.get("availability", "all")
    sort = request.GET.get("sort", "-created_at")
    category_ids = request.GET.getlist("category")
    author_id = request.GET.get("author")
    
    # Get all categories for the filter sidebar
    categories = Category.objects.all()
    selected_categories = []

    # Base queryset with related fields
    books = Book.objects.select_related("category").prefetch_related("authors")

    # Apply filters
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(isbn__icontains=query) |
            Q(authors__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    if book_type != "all":
        books = books.filter(book_type=book_type)

    if availability == "available":
        books = books.filter(status="available")

    # Filter by category only if valid category IDs are provided
    if category_ids:
        valid_category_ids = []
        for cat_id in category_ids:
            try:
                if cat_id and cat_id.isdigit():  # Check if it's a non-empty string containing only digits
                    valid_category_ids.append(int(cat_id))
            except (ValueError, TypeError):
                continue
        
        if valid_category_ids:
            books = books.filter(category_id__in=valid_category_ids)
            selected_categories = valid_category_ids

    # Filter by author only if valid author ID is provided
    if author_id and author_id.isdigit():
        books = books.filter(authors__id=author_id)

    # Apply sorting
    if sort:
        books = books.order_by(sort)

    # Pagination
    paginator = Paginator(books, 12)  # Show 12 books per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Create the context dictionary
    context = {
        "books": page_obj,
        "categories": categories,
        "selected_categories": selected_categories,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "current_query": {
            "q": query,
            "type": book_type,
            "availability": availability,
            "sort": sort,
            "author": author_id
        }
    }

    return render(request, "books/book_list.html", context)


@login_required
def book_detail(request, pk):    # Get book with related data
    book = get_object_or_404(
        Book.objects.select_related("category").prefetch_related(
            "authors", "borrowings__user"
        ),
        pk=pk,
    )

    # Get similar books (same category or authors)
    similar_books = (
        Book.objects.select_related("category")
        .prefetch_related("authors")
        .filter(Q(category=book.category) | Q(authors__in=book.authors.all()))
        .exclude(pk=book.pk)
        .distinct()[:3]
    )

    # Check borrowing restrictions for authenticated users
    can_borrow = True
    borrow_restriction_message = ""
    is_ebook = book.book_type == 'ebook'
    
    if request.user.is_authenticated and not is_ebook:
        # Only apply borrowing restrictions to physical books
        # Check if user already has this book borrowed
        existing_borrowing = BookBorrowing.objects.filter(
            user=request.user,
            book=book,
            status='active',
            returned_date__isnull=True
        ).exists()
        
        if existing_borrowing:
            can_borrow = False
            borrow_restriction_message = "You have already borrowed this book."
        else:
            # Check borrowing limit (maximum 2 books at a time)
            active_borrowings_count = BookBorrowing.objects.filter(
                user=request.user,
                status='active',
                returned_date__isnull=True
            ).count()
            
            if active_borrowings_count >= 2:
                can_borrow = False
                borrow_restriction_message = "You have reached the maximum borrowing limit of 2 books."

    context = {
        "book": book,
        "similar_books": similar_books,
        "can_borrow": can_borrow,
        "borrow_restriction_message": borrow_restriction_message,
        "is_ebook": is_ebook,
        "has_pdf": bool(book.pdf_file) if is_ebook else False,
    }
    return render(request, "books/book_detail.html", context)


@login_required
def borrow_book(request, pk):
    if request.method != "POST":
        return redirect("fbc_books:book_detail", pk=pk)

    book = get_object_or_404(Book, pk=pk)
    
    # Prevent borrowing of ebooks
    if book.book_type == 'ebook':
        messages.error(
            request,
            "E-books cannot be borrowed. You can read them online or download them instead."
        )
        return redirect("fbc_books:book_detail", pk=pk)

    # Check if book is available
    if book.status != "available" or book.available_copies < 1:
        messages.error(
            request,
            "Sorry, this book is currently not available for borrowing."
        )
        return redirect("fbc_books:book_detail", pk=pk)

    # Check if user already has this book borrowed (prevent duplicate borrowing)
    existing_borrowing = BookBorrowing.objects.filter(
        user=request.user,
        book=book,
        status='active',
        returned_date__isnull=True
    ).exists()
    
    if existing_borrowing:
        messages.error(
            request,
            f"You have already borrowed '{book.title}'. You cannot borrow the same book multiple times."
        )
        return redirect("fbc_books:book_detail", pk=pk)

    # Check borrowing limit (maximum 2 books at a time)
    active_borrowings_count = BookBorrowing.objects.filter(
        user=request.user,
        status='active',
        returned_date__isnull=True
    ).count()
    
    if active_borrowings_count >= 2:
        messages.error(
            request,
            f"You have reached the maximum borrowing limit of 2 books. Please return a book before borrowing another one."
        )
        return redirect("fbc_books:book_detail", pk=pk)

    # Create the borrowing
    due_date = timezone.now() + timezone.timedelta(days=14)  # 2 weeks
    borrowing = BookBorrowing.objects.create(
        book=book,
        user=request.user,
        due_date=due_date,
    )

    # Update book status and available copies
    book.available_copies -= 1
    book.update_status()

    messages.success(request, f"You have successfully borrowed {book.title}.")
    return redirect("fbc_books:dashboard")


@login_required
def my_books(request):
    # Get active and past borrowings
    active_borrowings = (
        BookBorrowing.objects.select_related("book")
        .filter(user=request.user, status="borrowed", returned_date__isnull=True)
        .order_by("due_date")
    )

    past_borrowings = (
        BookBorrowing.objects.select_related("book")
        .filter(user=request.user, returned_date__isnull=False)
        .order_by("-returned_date")
    )

    context = {
        "active_borrowings": active_borrowings,
        "past_borrowings": past_borrowings,
    }
    return render(request, "books/my_books.html", context)


@login_required
def read_ebook(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Check if book is an ebook
    if not book.is_ebook:
        messages.error(request, "This book is not available in e-book format.")
        return redirect("fbc_books:book_detail", pk=pk)

    # Check if user has active subscription
    if not request.user.is_subscription_active:
        messages.error(request, "Please activate your subscription to read e-books.")
        return redirect("fbc_books:book_detail", pk=pk)

    # Here you would typically handle the e-book viewer logic
    messages.success(request, "E-book viewer feature is coming soon!")
    return redirect("fbc_books:book_detail", pk=pk)


def is_lecturer_or_admin(user):
    return user.is_authenticated and (user.user_type == 'lecturer' or user.is_superuser)


@login_required
@user_passes_test(is_lecturer_or_admin)
def manage_books(request):
    books = Book.objects.all().order_by('-created_at')
    context = {
        'books': books,
        'title': 'Manage Books'
    }
    return render(request, 'books/manage_books.html', context)


def faq_view(request):
    """Display FAQ page with fine and payment information"""
    return render(request, 'books/faq.html')


@login_required
@user_passes_test(is_admin_or_staff)
def return_book(request, pk):
    if request.method != "POST":
        return redirect("fbc_users:admin_dashboard")

    borrowing = get_object_or_404(
        BookBorrowing.objects.select_related("book", "user"),
        pk=pk,
        status="active",
        returned_date__isnull=True
    )

    # Get the condition from POST data, defaulting to "good"
    condition = request.POST.get("condition", "good")
    
    # Mark the book as returned with the specified condition
    borrowing.mark_as_returned(condition=condition)

    messages.success(request, f"Book '{borrowing.book.title}' has been successfully returned by {borrowing.user.get_full_name()}.")
    return redirect("fbc_users:admin_dashboard")


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get summary statistics
    total_books = Book.objects.count()
    total_users = get_user_model().objects.count()
    active_borrowings = BookBorrowing.objects.filter(status='active').count()
    
    # Get overdue books count only (avoid calculating fines for now)
    overdue_count = BookBorrowing.objects.filter(
        status='active',
        due_date__lt=timezone.now()
    ).count()
    overdue_amount = 0  # Set to 0 to avoid calculation issues

    # Get additional comprehensive statistics
    available_books = total_books - active_borrowings
    pending_fines_count = Fine.objects.filter(status='pending').count()
    
    # Get today's returns (books due today)
    today = timezone.now().date()
    todays_returns = BookBorrowing.objects.filter(
        status='active',
        due_date__date=today
    ).count()

    # Get recent borrowings with related data
    recent_borrowings = (
        BookBorrowing.objects.select_related('book', 'user')
        .filter(status='active')
        .order_by('-borrowed_date')[:10]
    )

    # Get recent fines with explicit status filtering to avoid any field issues
    recent_fines = (
        Fine.objects.select_related('user', 'book')
        .filter(status='pending')  # Only pending fines to avoid any confusion
        .order_by('-date_issued')[:10]
    )
    
    context = {
        'total_books': total_books,
        'total_users': total_users,
        'active_borrowings': active_borrowings,
        'overdue_books': overdue_count,
        'overdue_amount': overdue_amount,
        'available_books': available_books,
        'pending_fines_count': pending_fines_count,
        'todays_returns': todays_returns,
        'recent_borrowings': recent_borrowings,
        'recent_fines': recent_fines,
        'today': today,
        'title': 'Admin Dashboard'
    }
    return render(request, 'books/admin_dashboard_simple.html', context)

@login_required
def user_dashboard(request):
    # Get user's books and activities
    active_borrowings = (
        BookBorrowing.objects.select_related('book')
        .filter(user=request.user, status='active')
        .order_by('due_date')
    )
    
    context = {
        'active_borrowings': active_borrowings,
        'title': 'My Dashboard'
    }
    
    return render(request, 'books/user_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    # Redirect to the enhanced fbc_users view
    return redirect('fbc_users:manage_users')

@login_required
@user_passes_test(is_admin)
def manage_borrowings(request):
    borrowings = BookBorrowing.objects.select_related('book', 'user').all()
    context = {
        'borrowings': borrowings,
        'title': 'Manage Borrowings'
    }
    return render(request, 'books/manage_borrowings.html', context)

@login_required
@user_passes_test(is_admin)
def process_return(request, borrowing_id):
    """Process a book return with condition assessment"""
    if request.method != 'POST':
        return redirect('fbc_users:admin_dashboard')

    borrowing = get_object_or_404(
        BookBorrowing.objects.select_related('book', 'user'),
        pk=borrowing_id,
        status='active'
    )

    # Get condition and notes from form
    condition = request.POST.get('condition', 'good')
    notes = request.POST.get('notes', '')

    # Process return based on condition
    if condition == 'good':
        # Normal return
        borrowing.mark_as_returned(condition=condition)
        messages.success(
            request, 
            f'Book "{borrowing.book.title}" returned successfully.'
        )
    elif condition in ['damaged', 'lost']:
        # Calculate penalty fine (book cost + Le 50)
        penalty_amount = borrowing.book.price + 50.00 if borrowing.book.price else 50.00
        
        # Create fine record
        Fine.objects.create(
            user=borrowing.user,
            book=borrowing.book,
            fine_type=condition,  # 'damaged' or 'lost'
            amount=penalty_amount,
            due_date=timezone.now() + timezone.timedelta(days=7),  # 1 week to pay
            notes=notes
        )
        
        # Update borrowing status
        borrowing.mark_as_returned(condition=condition)
        
        messages.warning(
            request,
            f'Book marked as {condition}. Fine of Le {penalty_amount} issued to {borrowing.user.get_full_name()}.',
        )

    return redirect('fbc_users:admin_dashboard')

@login_required
@user_passes_test(is_admin_or_staff)
def borrowing_detail(request, borrowing_id):
    """Display detailed information about a borrowing"""
    try:
        borrowing = get_object_or_404(
            BookBorrowing.objects.select_related('book', 'user'),
            pk=borrowing_id
        )

        # Check if this is an AJAX request
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
            # Return JSON data for AJAX requests
            # Get book authors
            authors = ', '.join([author.name for author in borrowing.book.authors.all()]) if borrowing.book.authors.exists() else 'Unknown'
            
            # Check if overdue
            is_overdue = borrowing.status == 'active' and borrowing.due_date < timezone.now()
            
            data = {
                'user': {
                    'full_name': borrowing.user.get_full_name(),
                    'username': borrowing.user.username,
                    'email': borrowing.user.email,
                    'user_type': dict(borrowing.user.USER_TYPE_CHOICES).get(borrowing.user.user_type, borrowing.user.user_type.title()),
                },
                'book': {
                    'title': borrowing.book.title,
                    'author': authors,
                    'isbn': borrowing.book.isbn,
                },
                'borrowed_date': borrowing.borrowed_date.strftime('%B %d, %Y'),
                'due_date': borrowing.due_date.strftime('%B %d, %Y'),
                'returned_date': borrowing.returned_date.strftime('%B %d, %Y') if borrowing.returned_date else None,
                'status': borrowing.status,
                'is_overdue': is_overdue,
                'fine_amount': float(borrowing.fine_amount) if borrowing.fine_amount else 0,
                'fine_paid': borrowing.fine_paid,
            }
            return JsonResponse(data)
        
        # For regular requests, return HTML template
        from fbc_fines.models import Fine
        fines = Fine.objects.filter(book=borrowing.book, user=borrowing.user)
        
        context = {
            'borrowing': borrowing,
            'fines': fines,
            'title': f'Borrowing Details: {borrowing.book.title}'
        }
        return render(request, 'books/borrowing_detail.html', context)
    
    except Exception as e:
        # Handle any errors gracefully
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        else:
            messages.error(request, f'Error loading borrowing details: {str(e)}')
            return redirect('fbc_books:manage_borrowings')


@login_required
@user_passes_test(is_admin_or_staff)
def attendance_log(request):
    # Example: show all users who entered the library today
    today = timezone.now().date()
    visitors = CustomUser.objects.filter(last_library_entry__date=today)
    context = {
        'visitors': visitors,
        'title': 'Attendance Log'
    }
    return render(request, 'books/attendance_log.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Book, Category
from django.urls import reverse

def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_admin)
def manage_books(request):
    """Enhanced manage books view with comprehensive statistics"""
    books = Book.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Calculate statistics
    total_books = books.count()
    available_books = books.filter(available_copies__gt=0).count()
    borrowed_books = books.filter(available_copies=0).count()
    damaged_books = books.filter(status='damaged').count()
    lost_books = books.filter(status='lost').count()
    
    context = {
        'books': books,
        'categories': categories,
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'damaged_books': damaged_books,
        'lost_books': lost_books,
        'title': 'Manage Books'
    }
    return render(request, 'books/manage_books.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def add_book(request):
    """Enhanced add book view with comprehensive field handling"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            authors_str = request.POST.get('authors', '')
            isbn = request.POST.get('isbn')
            category_id = request.POST.get('category')
            book_type = request.POST.get('book_type', 'physical')
            total_copies = int(request.POST.get('total_copies', 1))
            available_copies = int(request.POST.get('available_copies', 1))
            publication_year = request.POST.get('publication_year')
            description = request.POST.get('description', '')
            cover_image = request.FILES.get('cover_image')
            pdf_file = request.FILES.get('pdf_file')
            
            # Get category
            category = get_object_or_404(Category, id=category_id)

            # Validate ebook requires a PDF file
            if book_type == 'ebook' and not pdf_file:
                messages.error(request, 'Please upload an E-Book PDF file when selecting E-Book type.')
                categories = Category.objects.all()
                return render(request, 'books/add_book.html', {'categories': categories})
            
            # Create the book
            book = Book.objects.create(
                title=title,
                isbn=isbn,
                category=category,
                book_type=book_type,
                total_copies=total_copies,
                available_copies=available_copies,
                publication_year=int(publication_year) if publication_year else None,
                description=description,
                cover_image=cover_image,
                pdf_file=pdf_file if book_type == 'ebook' else None,
                status='available'
            )
            
            # Handle authors (create if they don't exist)
            if authors_str:
                author_names = [name.strip() for name in authors_str.split(',')]
                for author_name in author_names:
                    if author_name:
                        author, created = Author.objects.get_or_create(name=author_name)
                        book.authors.add(author)
            
            messages.success(request, f'Book "{title}" added successfully!')
            return redirect('fbc_books:manage_books')
            
        except Exception as e:
            messages.error(request, f'Error adding book: {str(e)}')
            # Fall through to render the form again with error
    
    # GET request or error - show the form
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'books/add_book.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
@login_required
@user_passes_test(is_staff_or_admin)
def edit_book(request, book_id):
    """Enhanced edit book view with comprehensive field handling"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        try:
            # Update basic fields
            book.title = request.POST.get('title', book.title)
            book.isbn = request.POST.get('isbn', book.isbn)
            book.description = request.POST.get('description', book.description)
            book.book_type = request.POST.get('book_type', book.book_type)
            book.total_copies = int(request.POST.get('total_copies', book.total_copies))
            book.available_copies = int(request.POST.get('available_copies', book.available_copies))
            
            # Update publication year
            publication_year = request.POST.get('publication_year')
            if publication_year:
                book.publication_year = int(publication_year)
            
            # Update category
            category_id = request.POST.get('category')
            if category_id:
                book.category = get_object_or_404(Category, id=category_id)
            
            # Handle cover image if provided
            cover_image = request.FILES.get('cover_image')
            if cover_image:
                book.cover_image = cover_image

            pdf_file = request.FILES.get('pdf_file')
            # If book type is ebook and a new pdf is provided, update it
            if book.book_type == 'ebook' and pdf_file:
                book.pdf_file = pdf_file
            # If switched to physical, clear any existing pdf_file
            elif book.book_type == 'physical':
                book.pdf_file = None
            
            book.save()
            
            # Handle authors update
            authors_str = request.POST.get('authors', '')
            if authors_str:
                # Clear existing authors and add new ones
                book.authors.clear()
                author_names = [name.strip() for name in authors_str.split(',')]
                for author_name in author_names:
                    if author_name:
                        author, created = Author.objects.get_or_create(name=author_name)
                        book.authors.add(author)
            
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('fbc_books:manage_books')
            
        except Exception as e:
            messages.error(request, f'Error updating book: {str(e)}')
            # Fall through to render the form again with error
    
    # GET request or error - show the form
    categories = Category.objects.all()
    context = {
        'book': book,
        'categories': categories,
    }
    return render(request, 'books/edit_book.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def delete_book(request, book_id):
    """Enhanced delete book view with proper confirmation"""
    if request.method == 'POST':
        try:
            book = get_object_or_404(Book, id=book_id)
            book_title = book.title
            book.delete()
            messages.success(request, f'Book "{book_title}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting book: {str(e)}')
    else:
        messages.error(request, 'Invalid request method for deleting book.')
    
    return redirect('fbc_books:manage_books')


@login_required
@user_passes_test(is_staff_or_admin)
def export_books(request):
    """Export books data to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fbc_library_books.csv"'
    
    writer = csv.writer(response)
    
    # Write CSV header
    writer.writerow([
        'Title', 'Authors', 'ISBN', 'Category', 'Book Type', 
        'Total Copies', 'Available Copies', 'Status', 
        'Description', 'Date Created'
    ])
    
    # Get all books with related data
    books = Book.objects.select_related('category').prefetch_related('authors').all()
    
    # Write book data
    for book in books:
        authors = ', '.join([author.name for author in book.authors.all()])
        writer.writerow([
            book.title,
            authors,
            book.isbn,
            book.category.name if book.category else 'N/A',
            book.get_book_type_display(),
            book.total_copies,
            book.available_copies,
            book.get_status_display(),
            book.description or 'N/A',
            book.created_at.strftime('%Y-%m-%d %H:%M') if book.created_at else 'N/A'
        ])
    
    return response

# E-book functionality views
@login_required
def ebook_preview(request, pk):
    """Preview an ebook in the browser"""
    book = get_object_or_404(Book, pk=pk, book_type='ebook')
    
    if not book.pdf_file:
        messages.error(request, 'This ebook is not available for preview.')
        return redirect('fbc_books:book_detail', pk=pk)
    
    context = {
        'book': book,
        'pdf_url': book.pdf_file.url,
        'title': f'Preview: {book.title}'
    }
    return render(request, 'books/ebook_preview.html', context)

@login_required
def ebook_download(request, pk):
    """Download an ebook"""
    from django.http import FileResponse, Http404
    import os
    
    book = get_object_or_404(Book, pk=pk, book_type='ebook')
    
    if not book.pdf_file:
        messages.error(request, 'This ebook is not available for download.')
        return redirect('fbc_books:book_detail', pk=pk)
    
    try:
        # Record the download activity
        from fbc_notifications.models import LibraryNotification
        LibraryNotification.objects.create(
            recipient=request.user,
            title=f'E-book Downloaded',
            message=f'You downloaded "{book.title}"',
            notification_type='ebook_download'
        )
        
        # Prepare file for download
        file_path = book.pdf_file.path
        if os.path.exists(file_path):
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=f"{book.title}.pdf"
            )
            return response
        else:
            messages.error(request, 'Ebook file not found.')
            return redirect('fbc_books:book_detail', pk=pk)
            
    except Exception as e:
        messages.error(request, f'Error downloading ebook: {str(e)}')
        return redirect('fbc_books:book_detail', pk=pk)

@login_required
def ebook_reader(request, pk):
    """Full-screen ebook reader"""
    book = get_object_or_404(Book, pk=pk, book_type='ebook')
    
    if not book.pdf_file:
        messages.error(request, 'This ebook is not available for reading.')
        return redirect('fbc_books:book_detail', pk=pk)
    
    context = {
        'book': book,
        'pdf_url': book.pdf_file.url,
        'title': f'Reading: {book.title}'
    }
    return render(request, 'books/ebook_reader.html', context)
