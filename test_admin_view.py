"""
Test view to check if the admin dashboard works without user objects
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from fbc_books.models import Book, BookBorrowing
from fbc_fines.models import Fine
from django.contrib.auth import get_user_model


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.user_type == "admin")


@login_required
@user_passes_test(is_admin)
def test_admin_dashboard(request):
    # Simple context without user objects
    context = {
        "total_books": Book.objects.count(),
        "total_users": get_user_model().objects.count(),
        "active_borrowings": BookBorrowing.objects.filter(status="active").count(),
        "overdue_books": 0,
        "overdue_amount": 0,
        "recent_borrowings": [],
        "recent_fines": [],
        "today": timezone.now().date(),
        "title": "Test Admin Dashboard",
    }
    return render(request, "books/admin_dashboard_simple.html", context)
