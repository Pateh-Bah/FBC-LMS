from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.conf import settings
import uuid
from .models import Payment, PaymentDetail
from fbc_books.models import BookBorrowing
from fbc_fines.models import Fine # Import Fine model
from fbc_users.models import CustomUser # Import CustomUser model


def is_staff_or_admin(user):
    return user.is_authenticated and user.user_type in ['admin', 'staff']


@login_required
@user_passes_test(is_staff_or_admin)
def manage_payments(request):
    payments = Payment.objects.all()
    context = {
        "payments": payments,
    }
    return render(request, "fbc_payments/manage_payments.html", context)


@login_required
@user_passes_test(is_staff_or_admin)
def add_payment(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        amount = request.POST.get("amount")
        payment_type = request.POST.get("payment_type")

        Payment.objects.create(
            user_id=user_id,
            amount=amount,
            payment_type=payment_type,
        )
        messages.success(request, "Payment added successfully!")
        return redirect("fbc_payments:manage_payments")
    return render(request, "fbc_payments/add_payment.html")


@login_required
@user_passes_test(is_staff_or_admin)
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == "POST":
        payment.amount = request.POST.get("amount")
        payment.payment_type = request.POST.get("payment_type")
        payment.save()
        messages.success(request, "Payment updated successfully!")
        return redirect("fbc_payments:manage_payments")
    return render(request, "fbc_payments/edit_payment.html", {"payment": payment})


@login_required
@user_passes_test(is_staff_or_admin)
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    messages.success(request, "Payment deleted successfully!")
    return redirect("fbc_payments:manage_payments")


@login_required
@user_passes_test(is_staff_or_admin)
def payment_details(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "fbc_payments/payment_details.html", {"payment": payment})


@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        payment_method = request.POST.get('payment_method')
        user = request.user
        amount = 0
        fine_id = request.POST.get('fine_id') # For fine payments

        if payment_type == 'subscription':
            if user.user_type != 'student':
                messages.error(request, "Subscriptions are only for students.")
                return redirect('fbc_users:profile')
            amount = getattr(settings, 'ANNUAL_SUBSCRIPTION_FEE', 50000) # Example fee
        elif payment_type == 'fine':
            if not fine_id:
                messages.error(request, "Fine ID not provided.")
                return redirect('fbc_fines:my_fines')
            try:
                fine_to_pay = Fine.objects.get(id=fine_id, user=user, status='pending')
                amount = fine_to_pay.amount
            except Fine.DoesNotExist:
                messages.error(request, "Fine not found or already paid.")
                return redirect('fbc_fines:my_fines')
        else:
            messages.error(request, "Invalid payment type.")
            return redirect('fbc_users:profile')

        if amount <= 0:
            messages.error(request, "Payment amount must be greater than zero.")
            return redirect('fbc_users:profile')

        # Create a pending payment record
        payment = Payment.objects.create(
            user=user,
            payment_type=payment_type,
            amount=amount,
            status="pending",
            payment_method=payment_method,
            transaction_id=f"SIM-{uuid.uuid4().hex[:10].upper()}"
        )

        if payment_type == 'fine' and fine_id:
            PaymentDetail.objects.create(
                payment=payment,
                fine_id=fine_id,
                reference=f"Fine payment for ID: {fine_id}"
            )
        
        # Store payment_id in session to retrieve after simulation
        request.session['payment_id_for_simulation'] = payment.id

        return redirect('fbc_payments:simulate_payment_form', payment_method=payment_method)

    # GET request: Show initial payment selection form
    user_fines = Fine.objects.filter(user=request.user, status='pending')
    context = {
        'user_fines': user_fines,
        'payment_methods': Payment.PAYMENT_METHODS,
        'show_subscription': request.user.user_type == 'student'
    }
    return render(request, 'payments/initiate_payment.html', context)

@login_required
def simulate_payment_form(request, payment_method):
    payment_id = request.session.get('payment_id_for_simulation')
    if not payment_id:
        messages.error(request, "No payment process initiated or session expired.")
        return redirect('fbc_payments:process_payment')

    try:
        payment = Payment.objects.get(id=payment_id, user=request.user, status='pending')
    except Payment.DoesNotExist:
        messages.error(request, "Payment record not found.")
        return redirect('fbc_payments:process_payment')

    if payment.payment_method != payment_method:
        messages.error(request, f"Payment method mismatch. Expected {payment.payment_method}, got {payment_method}")
        return redirect('fbc_payments:process_payment')

    context = {
        'payment': payment,
        'payment_method': payment_method,
    }
    template_name = f'payments/simulate_{payment_method}.html'
    # Check if specific template exists, else use a generic one or error
    try:
        return render(request, template_name, context)
    except Exception: # TemplateDoesNotExist
        messages.error(request, f"Simulation form for {payment_method} not found.")
        return redirect('fbc_payments:process_payment')

@login_required
def complete_simulated_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        # Add any specific field validation if needed, e.g. phone number for mobile money
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user, status='pending')
            
            # Simulate successful payment
            payment.mark_as_completed()
            payment.save()

            # Clear session variable
            if 'payment_id_for_simulation' in request.session:
                del request.session['payment_id_for_simulation']

            messages.success(request, f"Payment of {payment.amount} for {payment.get_payment_type_display()} via {payment.get_payment_method_display()} completed successfully!")
            if payment.payment_type == 'subscription':
                return redirect('fbc_users:my_subscription')
            elif payment.payment_type == 'fine':
                return redirect('fbc_fines:my_fines')
            return redirect('fbc_users:profile') # Fallback redirect
        except Payment.DoesNotExist:
            messages.error(request, "Payment record not found or already processed.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
    return redirect('fbc_payments:process_payment')


@login_required
@user_passes_test(is_staff_or_admin)
def payment_history(request):
    # Get query parameters
    payment_type = request.GET.get("payment_type")
    payment_method = request.GET.get("payment_method")
    status = request.GET.get("status")

    # Base queryset with related data - Show ALL payments for admin/staff
    payments = (
        Payment.objects.select_related("user")
        .prefetch_related("details", "details__borrowing", "details__borrowing__book")
        .all()  # Changed from filter(user=request.user) to show all payments
    )

    # Apply filters
    if payment_type:
        payments = payments.filter(payment_type=payment_type)
    if payment_method:
        payments = payments.filter(payment_method=payment_method)
    if status:
        payments = payments.filter(status=status)

    # Order by latest first
    payments = payments.order_by("-created_at")

    # Pagination
    paginator = Paginator(payments, 15)  # Show 15 payments per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "payments": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    }
    return render(request, "payments/history.html", context)


@login_required
def my_payments(request):
    """Display user's payment history"""
    # Get query parameters for filtering
    payment_type = request.GET.get("payment_type")
    payment_method = request.GET.get("payment_method")
    status = request.GET.get("status")

    # Base queryset with related data
    payments = (
        Payment.objects.select_related("user")
        .prefetch_related("details", "details__borrowing", "details__borrowing__book")
        .filter(user=request.user)
    )

    # Apply filters
    if payment_type:
        payments = payments.filter(payment_type=payment_type)
    if payment_method:
        payments = payments.filter(payment_method=payment_method)
    if status:
        payments = payments.filter(status=status)

    # Order by latest first
    payments = payments.order_by("-created_at")

    # Pagination
    paginator = Paginator(payments, 10)  # Show 10 payments per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "payments": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "payment_types": Payment.PAYMENT_TYPES,
        "payment_methods": Payment.PAYMENT_METHODS,
        "payment_statuses": Payment.PAYMENT_STATUS,
        "current_filters": {
            "payment_type": payment_type,
            "payment_method": payment_method,
            "status": status,
        }
    }
    return render(request, "payments/my_payments.html", context)
