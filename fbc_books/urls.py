from django.urls import path
from . import views

app_name = 'fbc_books'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/my-books/', views.my_books, name='my_books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),  # Added this pattern
    path('books/borrowing/<int:pk>/return/', views.return_book, name='return_book'),  # Added this pattern
    path('books/manage/', views.manage_books, name='manage_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('books/details/<int:book_id>/', views.book_detail, name='book_details'),  # Fixed view name
    path('faq/', views.faq_view, name='faq'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('manage/books/', views.manage_books, name='manage_books'),
    path('manage/books/export/', views.export_books, name='export_books'),
    path('manage/users/', views.manage_users, name='manage_users'),  # This redirects to fbc_users
    path('manage/borrowings/', views.manage_borrowings, name='manage_borrowings'),
    # Add new URL patterns
    path('manage/borrowing/<int:borrowing_id>/return/', views.process_return, name='process_return'),
    path('manage/borrowing/<int:borrowing_id>/', views.borrowing_detail, name='borrowing_detail'),
    path('manage/attendance-log/', views.attendance_log, name='attendance_log'),
    # E-book specific URLs
    path('books/<int:pk>/preview/', views.ebook_preview, name='ebook_preview'),
    path('books/<int:pk>/download/', views.ebook_download, name='ebook_download'),
    path('books/<int:pk>/read/', views.ebook_reader, name='ebook_reader'),
]
