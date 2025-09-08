from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from decimal import Decimal
from .models import Fine
from .forms import FineForm
from fbc_payments.models import Payment, PaymentDetail

def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def fine_list(request):
    """Display list of user's fines"""
    user_fines = Fine.objects.filter(user=request.user)
    return render(request, 'fbc_fines/fine_list.html', {
        'fines': user_fines
    })

@login_required
def fine_detail(request, pk):
    """Display fine details"""
    fine = get_object_or_404(Fine, pk=pk)
    if request.user != fine.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this fine.")
        return redirect('fbc_fines:fine_list')
    return render(request, 'fbc_fines/fine_detail.html', {
        'fine': fine
    })

@login_required
def pay_fine(request, pk):
    """Process fine payment"""
    fine = get_object_or_404(Fine, pk=pk)
    if request.user != fine.user:
        messages.error(request, "You don't have permission to pay this fine.")
        return redirect('fbc_fines:fine_list')
    
    if request.method == "POST":
        # Payment processing logic will go here
        # This is a placeholder for now
        fine.status = 'paid'
        fine.payment_date = timezone.now()
        fine.save()
        messages.success(request, "Fine has been paid successfully.")
        return redirect('fbc_fines:fine_detail', pk=fine.pk)
        
    return render(request, 'fbc_fines/pay_fine.html', {
        'fine': fine
    })

@login_required
def create_fine(request):
    """Create a new fine"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create fines.")
        return redirect('fbc_fines:fine_list')
        
    if request.method == "POST":
        form = FineForm(request.POST)
        if form.is_valid():
            fine = form.save(commit=False)
            fine.save()
            messages.success(request, "Fine created successfully.")
            return redirect('fbc_fines:fine_detail', pk=fine.pk)
    else:
        form = FineForm()
    
    return render(request, 'fbc_fines/create_fine.html', {
        'form': form,
        'title': 'Create Fine'
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def verify_payment(request, pk):
    """Verify a fine payment with provided reference"""
    if request.method != 'POST':
        return redirect('fbc_fines:fine_detail', pk=pk)

    fine = get_object_or_404(Fine, pk=pk, status='pending')

    # Get payment details from form
    payment_method = request.POST.get('payment_method')
    payment_reference = request.POST.get('payment_reference')
    notes = request.POST.get('notes', '')

    if not payment_method or not payment_reference:
        messages.error(request, 'Please provide payment method and reference.')
        return redirect('fbc_fines:fine_detail', pk=pk)

    # Create payment record
    payment = Payment.objects.create(
        user=fine.user,
        payment_type='fine',
        amount=fine.amount,
        payment_method=payment_method,
        status='completed',
        transaction_id=payment_reference
    )

    # Update fine status
    fine.status = 'paid'
    fine.payment_method = payment_method
    fine.payment_reference = payment_reference
    fine.payment_date = timezone.now()
    fine.notes = (fine.notes + '\n' + notes).strip()
    fine.save()

    # Create payment detail record
    PaymentDetail.objects.create(
        payment=payment,
        borrowing=fine.book.borrowings.filter(user=fine.user).latest('borrowed_date'),
        reference=f'Fine payment for {fine.book.title}'
    )

    messages.success(request, f'Payment of Le {fine.amount} verified successfully.')
    return redirect('fbc_books:admin_dashboard')

@login_required
@user_passes_test(is_staff_or_admin)
def manage_fines(request):
    """Admin view for managing fines"""
    from django.contrib.auth import get_user_model
    from fbc_books.models import Book
    from django.core.paginator import Paginator
    
    User = get_user_model()
    
    # Handle POST request for adding new fine
    if request.method == 'POST':
        user_id = request.POST.get('user')
        book_id = request.POST.get('book')
        fine_type = request.POST.get('fine_type', 'general')
        amount = request.POST.get('amount')
        reason = request.POST.get('reason', '')
        
        try:
            # Validate required fields
            if not user_id:
                messages.error(request, 'User is required.')
                return redirect('fbc_fines:manage_fines')
            
            if not amount:
                messages.error(request, 'Amount is required.')
                return redirect('fbc_fines:manage_fines')
            
            # Convert amount to decimal
            try:
                amount_decimal = Decimal(str(amount))
                if amount_decimal <= 0:
                    messages.error(request, 'Amount must be greater than zero.')
                    return redirect('fbc_fines:manage_fines')
            except (ValueError, TypeError):
                messages.error(request, 'Invalid amount format.')
                return redirect('fbc_fines:manage_fines')
            
            # Get user
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                messages.error(request, 'Selected user not found.')
                return redirect('fbc_fines:manage_fines')
            
            # Get book if provided
            book = None
            if book_id:
                try:
                    book = Book.objects.get(id=book_id)
                except Book.DoesNotExist:
                    messages.error(request, 'Selected book not found.')
                    return redirect('fbc_fines:manage_fines')
            
            # Create the fine
            fine = Fine.objects.create(
                user=user,
                book=book,
                fine_type=fine_type,
                amount=amount_decimal,
                reason=reason,
                status='pending'
            )
            
            user_display = user.get_full_name() or user.username
            book_display = f" for {book.title}" if book else ""
            messages.success(request, f'Fine of Le {amount} added for {user_display}{book_display}')
            
        except Exception as e:
            messages.error(request, f'Error adding fine: {str(e)}')
        
        return redirect('fbc_fines:manage_fines')
    
    # Get query parameters for filtering
    payment_status = request.GET.get('status', 'all')
    fine_type = request.GET.get('type', 'all')
    search_query = request.GET.get('search', '')

    # Start with all fines and related data
    fines = Fine.objects.select_related('user', 'book')

    # Apply search filter
    if search_query:
        fines = fines.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(book__title__icontains=search_query) |
            Q(reason__icontains=search_query)
        )

    # Apply filters
    if payment_status != 'all':
        fines = fines.filter(status=payment_status)
    if fine_type != 'all':
        fines = fines.filter(fine_type=fine_type)

    # Order by most recent first
    fines = fines.order_by('-date_issued')

    # Pagination
    paginator = Paginator(fines, 25)  # Show 25 fines per page
    page_number = request.GET.get('page')
    fines_page = paginator.get_page(page_number)

    # Calculate summary statistics
    all_fines = Fine.objects.all()
    total_outstanding = (
        all_fines.filter(status='pending')
        .aggregate(total=Sum('amount'))['total'] or 0
    )
    total_collected = (
        all_fines.filter(status='paid')
        .aggregate(total=Sum('amount'))['total'] or 0
    )
    pending_count = all_fines.filter(status='pending').count()
    total_fines = all_fines.count()

    # Get all users and books for the add fine form
    users = User.objects.filter(is_active=True).order_by('first_name', 'last_name', 'username')
    books = Book.objects.all().order_by('title')

    context = {
        'fines': fines_page,
        'payment_status': payment_status,
        'fine_type': fine_type,
        'search_query': search_query,
        'total_outstanding': total_outstanding,
        'total_collected': total_collected,
        'pending_count': pending_count,
        'total_fines': total_fines,
        'users': users,
        'books': books,
        'title': 'Manage Fines'
    }
    return render(request, 'fbc_fines/manage_fines.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def add_fine(request):
    if request.method == 'POST':
        form = FineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fine added successfully!')
            return redirect('fbc_fines:manage_fines')
    else:
        form = FineForm()
    return render(request, 'fbc_fines/add_fine.html', {'form': form})

@login_required
@user_passes_test(is_staff_or_admin)
def edit_fine(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    if request.method == 'POST':
        form = FineForm(request.POST, instance=fine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fine updated successfully!')
            return redirect('fbc_fines:manage_fines')
    else:
        form = FineForm(instance=fine)
    return render(request, 'fbc_fines/edit_fine.html', {'form': form, 'fine': fine})

@login_required
@user_passes_test(is_staff_or_admin)
def delete_fine(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    fine.delete()
    messages.success(request, 'Fine deleted successfully!')
    return redirect('fbc_fines:manage_fines')

@login_required
@user_passes_test(is_staff_or_admin)
@login_required
def fine_details(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    # Check permission - users can only view their own fines, staff can view all
    if request.user != fine.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this fine.")
        return redirect('fbc_fines:my_fines')
    return render(request, 'fbc_fines/fine_details.html', {
        'fine': fine,
        'today': timezone.now().date()
    })

@login_required
def my_fines(request):
    """Display current user's fines"""
    fines = Fine.objects.filter(user=request.user).order_by('-date_issued')
    
    # Calculate totals
    total_fines = fines.aggregate(total=Sum('amount'))['total'] or 0
    pending_fines = fines.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    paid_fines = fines.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'fines': fines,
        'total_fines': total_fines,
        'pending_fines': pending_fines,
        'paid_fines': paid_fines,
        'today': timezone.now().date(),
        'title': 'My Fines'
    }
    return render(request, 'fbc_fines/my_fines.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def mark_fine_paid(request, fine_id):
    """AJAX view to mark a fine as paid"""
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            fine = get_object_or_404(Fine, id=fine_id)
            fine.status = 'paid'
            fine.payment_date = timezone.now()
            fine.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Fine of Le {fine.amount} marked as paid'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error marking fine as paid: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
@user_passes_test(is_staff_or_admin)
def delete_fine(request, fine_id):
    """AJAX view to delete a fine"""
    from django.http import JsonResponse
    
    if request.method == 'DELETE':
        try:
            fine = get_object_or_404(Fine, id=fine_id)
            amount = fine.amount
            user_name = fine.user.get_full_name() or fine.user.username
            fine.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Fine of Le {amount} for {user_name} deleted successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error deleting fine: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
@user_passes_test(is_staff_or_admin)
def export_fines(request):
    """Export fines to CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fines_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['User', 'Email', 'Book', 'Amount', 'Date Issued', 'Status', 'Reason'])
    
    fines = Fine.objects.select_related('user', 'book').order_by('-date_issued')
    for fine in fines:
        writer.writerow([
            fine.user.get_full_name() or fine.user.username,
            fine.user.email,
            fine.book.title if fine.book else 'N/A',
            fine.amount,
            fine.date_issued.strftime('%Y-%m-%d'),
            fine.status.title(),
            fine.reason or 'N/A'
        ])
    
    return response
