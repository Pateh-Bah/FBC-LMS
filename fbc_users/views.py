from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
import logging

# Configure logging for authentication events
logger = logging.getLogger(__name__)

from .models import CustomUser
from .decorators import (
    database_verified_login_required, 
    user_type_required, 
    admin_required, 
    staff_or_admin_required,
    active_subscription_required
)
from fbc_books.models import Book, BookBorrowing
from fbc_fines.models import Fine
from fbc_notifications.models import LibraryNotification
from fbc_payments.models import Payment
from .system_settings import SystemSettings
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def get_client_ip(request):
    """Get the client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def user_login(request):
    """Handle user login"""
    if request.user.is_authenticated:
        # Redirect based on user type to appropriate dashboards
        if request.user.user_type == 'admin':
            return redirect('fbc_users:admin_dashboard')
        elif request.user.user_type == 'staff':
            return redirect('fbc_users:staff_dashboard_beautiful')
        elif request.user.user_type == 'lecturer':
            return redirect('fbc_users:lecturer_dashboard')
        elif request.user.user_type == 'student':
            return redirect('fbc_users:student_dashboard')
        else:
            return redirect('fbc_users:student_dashboard')  # Default fallback
            
    # Clear any existing messages for GET requests to prevent showing admin action messages on login page
    # But preserve logout messages from the logout redirect
    if request.method == 'GET':
        # Check if we're coming from logout based on the URL or session
        referer = request.META.get('HTTP_REFERER', '')
        coming_from_logout = 'logout' in referer or request.session.get('just_logged_out', False)
        
        if not coming_from_logout:
            # Clear messages only if NOT coming from logout
            storage = messages.get_messages(request)
            # Consume all messages to clear them
            for message in storage:
                pass
        else:
            # Clear the session flag
            request.session.pop('just_logged_out', None)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        client_ip = get_client_ip(request)
        
        # Log all login attempts
        logger.info(f"Login attempt for username: {username} from IP: {client_ip}")
        
        if not username or not password:
            logger.warning(f"Empty credentials submitted from IP: {client_ip}")
            messages.error(request, 'Please enter both username and password.')
            return redirect('fbc_users:login')
        
        # Authenticate against database only
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Double-check user exists in database and is valid
            try:
                db_user = CustomUser.objects.get(id=user.id, username=username)
                
                if db_user.is_suspended:
                    logger.warning(f"Suspended user {username} attempted login from IP: {client_ip}")
                    messages.error(request, 'Your account is suspended. Please contact the administrator.')
                elif not db_user.is_active:
                    logger.warning(f"Inactive user {username} attempted login from IP: {client_ip}")
                    messages.warning(request, 'Your account is not active. Please contact the administrator.')
                else:
                    # Successful authentication - log and proceed
                    logger.info(f"Successful login for user {username} ({db_user.user_type}) from IP: {client_ip}")
                    
                    # Set the backend attribute to fix multiple backends issue
                    db_user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, db_user)
                    
                    # Update last activity
                    db_user.last_activity = timezone.now()
                    db_user.save(update_fields=['last_activity'])
                    
                    messages.success(request, f'Welcome back, {db_user.get_full_name() or db_user.username}!')
                    
                    # Redirect based on user type to custom dashboards
                    if db_user.user_type == 'admin':
                        return redirect('fbc_users:admin_dashboard')
                    elif db_user.user_type == 'staff':
                        return redirect('fbc_users:staff_dashboard_beautiful')
                    elif db_user.user_type == 'lecturer':
                        return redirect('fbc_users:lecturer_dashboard')
                    else:  # student
                        return redirect('fbc_users:student_dashboard')
                        
            except CustomUser.DoesNotExist:
                # This should never happen if authenticate() worked, but adding as safety
                logger.error(f"Authentication succeeded but user {username} not found in database")
                messages.error(request, 'Authentication error. Please try again.')
        else:
            logger.warning(f"Failed login attempt for username: {username} from IP: {client_ip}")
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')


def login_view(request):
    return user_login(request)


@user_type_required('student')
def student_dashboard(request):

    # Get user activities
    active_borrowings = BookBorrowing.objects.filter(
        user=request.user,
        status='active'
    ).select_related('book')

    total_fines = Fine.objects.filter(
        user=request.user,
        status='pending'
    ).aggregate(total=Sum('amount'))['total'] or 0

    books_returned = BookBorrowing.objects.filter(
        user=request.user,
        status='returned'
    ).count()

    subscription_days_left = 0
    if request.user.subscription_end_date:
        days_left = (request.user.subscription_end_date - timezone.now()).days
        subscription_days_left = max(0, days_left)

    recent_activities = LibraryNotification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')[:5]

    context = {
        'active_borrowings': active_borrowings,
        'total_fines': total_fines,
        'books_returned': books_returned,
        'subscription_days_left': subscription_days_left,
        'recent_activities': recent_activities,
        'title': 'Student Dashboard'
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@user_type_required('lecturer')
def lecturer_dashboard(request):

    active_borrowings = BookBorrowing.objects.filter(
        user=request.user,
        status='active'
    ).select_related('book')

    total_fines = Fine.objects.filter(
        user=request.user,
        status='pending'
    ).aggregate(total=Sum('amount'))['total'] or 0

    books_returned = BookBorrowing.objects.filter(
        user=request.user,
        status='returned'
    ).count()

    subscription_days_left = 0
    if hasattr(request.user, 'subscription_end_date') and request.user.subscription_end_date:
        days_left = (request.user.subscription_end_date - timezone.now()).days
        subscription_days_left = max(0, days_left)

    recent_activities = LibraryNotification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')[:5]

    context = {
        'active_borrowings': active_borrowings,
        'total_fines': total_fines,
        'books_returned': books_returned,
        'subscription_days_left': subscription_days_left,
        'recent_activities': recent_activities,
        'title': 'Lecturer Dashboard',
        'user': request.user,
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@user_type_required('staff')
def staff_dashboard(request):
    """Enhanced dashboard for staff users"""
    # Book management statistics
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='available').count()
    borrowed_books = Book.objects.filter(status='borrowed').count()
    overdue_books = BookBorrowing.objects.filter(
        status='active',
        due_date__lt=timezone.now()
    ).count()
    
    # Daily statistics
    today = timezone.now().date()
    daily_borrows = BookBorrowing.objects.filter(borrowed_date__date=today).count()
    daily_returns = BookBorrowing.objects.filter(
        returned_date__date=today,
        status='returned'
    ).count()
    
    # User management
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    
    # Recent activities
    recent_borrowings = BookBorrowing.objects.select_related('user', 'book').order_by('-borrowed_date')[:10]
    recent_returns = BookBorrowing.objects.filter(
        status='returned'
    ).select_related('user', 'book').order_by('-returned_date')[:10]
    
    # Fine management
    pending_fines = Fine.objects.filter(status='pending').count()
    total_pending_fines = Fine.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    
    # Additional metrics for staff dashboard
    pending_returns = BookBorrowing.objects.filter(status='active').count()
    
    # Recent notifications
    recent_notifications = LibraryNotification.objects.filter(
        Q(notification_type='book_borrowed') |
        Q(notification_type='book_returned') |
        Q(notification_type='fine_issued')
    ).order_by('-created_at')[:10]
    
    context = {
        'title': 'Staff Dashboard',
        'user': request.user,
        
        # Book statistics
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'overdue_books': overdue_books,
        
        # Daily stats
        'daily_borrows': daily_borrows,
        'daily_returns': daily_returns,
        
        # User stats
        'total_users': total_users,
        'active_users': active_users,
        
        # Fine management
        'pending_fines': pending_fines,
        'total_pending_fines': total_pending_fines,
        
        # Additional metrics
        'pending_returns': pending_returns,
        
        # Recent activities
        'recent_borrowings': recent_borrowings,
        'recent_returns': recent_returns,
        'recent_notifications': recent_notifications,
        
    # Quick actions data
    'can_manage_books': True,
    'can_manage_users': True,
    'can_manage_fines': True,
    }
    
    return render(request, 'users/staff_dashboard.html', context)


@user_type_required('staff')
def staff_dashboard_beautiful(request):
    """
    Beautiful staff dashboard with the same UI as admin dashboard
    But with restricted permissions for user management and system settings
    """
    from fbc_books.models import Book, BookBorrowing
    from fbc_fines.models import Fine
    
    # System statistics (same as admin)
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    suspended_users = CustomUser.objects.filter(is_suspended=True).count()
    
    # User type breakdown
    admin_users = CustomUser.objects.filter(user_type='admin').count()
    staff_users = CustomUser.objects.filter(user_type='staff').count()
    lecturer_users = CustomUser.objects.filter(user_type='lecturer').count()
    student_users = CustomUser.objects.filter(user_type='student').count()
    
    # Book statistics
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='available').count()
    borrowed_books = Book.objects.filter(status='borrowed').count()
    
    # Recent activities
    recent_borrowings = BookBorrowing.objects.select_related('user', 'book').order_by('-borrowed_date')[:10]
    recent_users = CustomUser.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=7)).order_by('-date_joined')[:5]
    
    # Financial statistics
    total_fines = Fine.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    total_payments = Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent notifications
    recent_notifications = LibraryNotification.objects.order_by('-created_at')[:10]
    
    # System health check
    today = timezone.now().date()
    daily_logins = CustomUser.objects.filter(last_activity__date=today).count()
    
    context = {
        'title': 'Staff Dashboard',
        'user': request.user,
        
        # User statistics
        'total_users': total_users,
        'active_users': active_users,
        'suspended_users': suspended_users,
        'admin_users': admin_users,
        'staff_users': staff_users,
        'lecturer_users': lecturer_users,
        'student_users': student_users,
        
        # Book statistics
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        
        # Financial data
        'total_fines': total_fines,
        'total_payments': total_payments,
        
        # Recent activities
        'recent_borrowings': recent_borrowings,
        'recent_users': recent_users,
        'recent_notifications': recent_notifications,
        
        # System health
        'daily_logins': daily_logins,
        
        # Quick stats for charts
        'user_type_data': {
            'admin': admin_users,
            'staff': staff_users,
            'lecturer': lecturer_users,
            'student': student_users,
        },
        
        'book_status_data': {
            'available': available_books,
            'borrowed': borrowed_books,
        },
        
    # Staff-specific flags
    'is_staff': True,
    'can_manage_users': True,
    'can_manage_system_settings': False,
    }
    return render(request, 'users/staff_dashboard_beautiful.html', context)


@admin_required
def admin_dashboard(request):
    """Comprehensive dashboard for admin users"""
    # System statistics
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    suspended_users = CustomUser.objects.filter(is_suspended=True).count()
    
    # User type breakdown
    admin_users = CustomUser.objects.filter(user_type='admin').count()
    staff_users = CustomUser.objects.filter(user_type='staff').count()
    lecturer_users = CustomUser.objects.filter(user_type='lecturer').count()
    student_users = CustomUser.objects.filter(user_type='student').count()
    
    # Book statistics
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='available').count()
    borrowed_books = Book.objects.filter(status='borrowed').count()
    
    # Recent activities
    recent_borrowings = BookBorrowing.objects.select_related('user', 'book').order_by('-borrowed_date')[:10]
    recent_users = CustomUser.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=7)).order_by('-date_joined')[:5]
    
    # Financial statistics
    total_fines = Fine.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    total_payments = Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent notifications
    recent_notifications = LibraryNotification.objects.order_by('-created_at')[:10]
    
    # System health check
    today = timezone.now().date()
    daily_logins = CustomUser.objects.filter(last_activity__date=today).count()
    
    context = {
        'title': 'Admin Dashboard',
        'user': request.user,
        
        # User statistics
        'total_users': total_users,
        'active_users': active_users,
        'suspended_users': suspended_users,
        'admin_users': admin_users,
        'staff_users': staff_users,
        'lecturer_users': lecturer_users,
        'student_users': student_users,
        
        # Book statistics
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        
        # Financial data
        'total_fines': total_fines,
        'total_payments': total_payments,
        
        # Recent activities
        'recent_borrowings': recent_borrowings,
        'recent_users': recent_users,
        'recent_notifications': recent_notifications,
        
        # System health
        'daily_logins': daily_logins,
        
        # Quick stats for charts
        'user_type_data': {
            'admin': admin_users,
            'staff': staff_users,
            'lecturer': lecturer_users,
            'student': student_users,
        },
        
        'book_status_data': {
            'available': available_books,
            'borrowed': borrowed_books,
        }
    }
    
    return render(request, 'users/admin_dashboard.html', context)


def user_logout(request):
    if request.user.is_authenticated:
        # Log the logout activity
        request.user.last_activity = timezone.now()
        request.user.save()
    # Clear any existing queued messages to avoid duplicates
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    logout(request)
    # Set a session flag to indicate we just logged out
    request.session['just_logged_out'] = True
    # Add logout message and redirect immediately
    messages.success(request, "Successfully logged out.")
    return redirect('fbc_users:login')


@login_required
def user_profile(request):
    """Display user profile page"""
    context = {
        'user': request.user,
        'title': 'My Profile',
        'active_tab': 'profile'
    }
    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('fbc_users:profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})


def password_reset(request):
    """Handle password reset requests"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build the reset URL
            reset_url = request.build_absolute_uri(
                reverse('fbc_users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Send email
            send_mail(
                'Password Reset Request',
                f'Please click the following link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, "Password reset instructions have been sent to your email.")
            return redirect('fbc_users:login')
        except CustomUser.DoesNotExist:
            messages.error(request, "No user found with that email address.")
    
    return render(request, 'users/password_reset.html')


def is_staff_or_admin(user):
    return user.is_authenticated and user.user_type in ['admin', 'staff']

def is_admin_only(user):
    """Only admin users can perform CRUD operations"""
    return user.is_authenticated and user.user_type == 'admin'

@login_required
@user_passes_test(is_staff_or_admin)
def manage_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Calculate statistics
    total_users = users.count()
    active_users = users.filter(is_suspended=False).count()
    student_count = users.filter(user_type='student').count()
    staff_count = users.filter(user_type__in=['staff', 'admin', 'lecturer']).count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'student_count': student_count,
        'staff_count': staff_count,
        'title': 'Manage Library Members'
    }
    return render(request, 'users/manage_users.html', context)

def can_add_user_type(request_user, target_user_type):
    """Check if the requesting user can add users of the specified type"""
    if request_user.user_type == 'admin':
        return True  # Admin can add any user type
    elif request_user.user_type == 'staff':
        # Staff can add only students and lecturers
        return target_user_type in ['student', 'lecturer']
    return False

@login_required
@user_passes_test(is_staff_or_admin)
def add_user(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user_type = request.POST.get('user_type', 'student')
        university_id = request.POST.get('university_id', '')
        phone_number = request.POST.get('phone_number', '')
        profile_image = request.FILES.get('profile_image')
        
        # Check if user can add this user type
        if not can_add_user_type(request.user, user_type):
            messages.error(request, 'You do not have permission to create admin users.')
            return redirect('fbc_users:manage_users')
        
        try:
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                university_id=university_id,
                phone_number=phone_number,
            )
            
            if profile_image:
                user.profile_image = profile_image
                user.save()
            
            messages.success(request, f'User {user.get_full_name()} added successfully!')
            logger.info(f"User {user.username} created by {request.user.username}")
            return redirect('fbc_users:manage_users')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            logger.error(f"Error creating user: {str(e)}")
    
    return render(request, 'users/add_user.html')

def can_edit_user(request_user, target_user):
    """Check if the requesting user can edit the target user"""
    if request_user.user_type == 'admin':
        return True  # Admin can edit any user
    elif request_user.user_type == 'staff':
        # Staff may edit students and lecturers; allow editing self
        if request_user.id == target_user.id:
            return True
        return target_user.user_type in ['student', 'lecturer']
    return False

def can_delete_user(request_user, target_user):
    """Check if the requesting user can delete the target user"""
    if request_user.user_type == 'admin':
        return True  # Admin can delete any user (except themselves, handled elsewhere)
    elif request_user.user_type == 'staff':
        # Staff can only delete students and lecturers
        return target_user.user_type in ['student', 'lecturer']
    return False

@login_required
@user_passes_test(is_staff_or_admin)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Check if user can edit this user
    if not can_edit_user(request.user, user):
        messages.error(request, 'You do not have permission to edit admin users.')
        return redirect('fbc_users:manage_users')
    
    if request.method == 'POST':
        # Block staff from editing admin users via form submission
        if request.POST.get('restricted_edit') == 'true':
            messages.error(request, 'You do not have permission to edit admin users.')
            return redirect('fbc_users:manage_users')
            
        try:
            # Update basic information
            new_first_name = request.POST.get('first_name', '').strip()
            new_last_name = request.POST.get('last_name', '').strip()
            new_username = request.POST.get('username', user.username).strip()
            new_email = request.POST.get('email', user.email).strip()
            user.university_id = request.POST.get('university_id', '').strip()
            user.phone_number = request.POST.get('phone_number', '').strip()
            
            # Validate required fields
            if not new_username:
                raise ValueError("Username is required")
            if not new_email:
                raise ValueError("Email is required")

            # Ensure username/email are unique for other users
            if CustomUser.objects.exclude(id=user.id).filter(username=new_username).exists():
                raise ValueError("Username is already taken")
            if CustomUser.objects.exclude(id=user.id).filter(email=new_email).exists():
                raise ValueError("Email is already in use")

            user.first_name = new_first_name
            user.last_name = new_last_name
            user.username = new_username
            user.email = new_email
            
            # Update user type - check permissions
            new_user_type = request.POST.get('user_type', user.user_type)
            if request.user.user_type == 'admin':
                user.user_type = new_user_type  # Admin can change to any type
            elif request.user.user_type == 'staff':
                # Staff can only set user type to student or lecturer (and not elevate to admin/staff)
                if user.user_type in ['student', 'lecturer'] or request.user.id == user.id:
                    if new_user_type in ['student', 'lecturer']:
                        user.user_type = new_user_type
            
            # Update suspension status (admin only)
            if request.user.user_type == 'admin':
                is_suspended_val = str(request.POST.get('is_suspended', '')).lower()
                is_suspended = is_suspended_val in ['true', 'on', '1', 'yes']
                user.is_suspended = is_suspended
            
            # Handle profile image
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                user.profile_image = profile_image
            
            # Handle password change
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_new_password', '').strip()
            
            password_changed = False
            if new_password:
                if len(new_password) < 8:
                    raise ValueError("Password must be at least 8 characters long")
                if new_password != confirm_password:
                    raise ValueError("Passwords do not match")
                user.set_password(new_password)
                password_changed = True
            
            user.save()

            # Preserve session if the user edited their own password
            if password_changed and request.user.id == user.id:
                update_session_auth_hash(request, user)
            
            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f'User {user.get_full_name()} updated successfully!'
                })
            
            messages.success(request, f'User {user.get_full_name()} updated successfully!')
            logger.info(f"User {user.username} updated by {request.user.username}")
            return redirect('fbc_users:manage_users')
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error updating user {user.username}: {error_message}")
            
            # If it's an AJAX request, return JSON error response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': error_message
                }, status=400)
            
            messages.error(request, f'Failed to update member: {error_message}')
    
    return render(request, 'users/edit_user.html', {
        'user': user,
        'can_edit_user_type': request.user.user_type == 'admin' or (request.user.user_type == 'staff' and user.user_type in ['student', 'lecturer']),
        'can_suspend': request.user.user_type == 'admin'
    })

@login_required
@user_passes_test(is_staff_or_admin)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent users from deleting themselves
    if user.id == request.user.id:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('fbc_users:manage_users')
    
    # Check if user can delete this user
    if not can_delete_user(request.user, user):
        messages.error(request, 'You do not have permission to delete admin users.')
        return redirect('fbc_users:manage_users')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        logger.info(f"User {username} deleted by {request.user.username}")
        return redirect('fbc_users:manage_users')
    
    return redirect('fbc_users:manage_users')

@login_required
@user_passes_test(is_staff_or_admin)
def user_details(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Get related data
    from fbc_books.models import BookBorrowing
    from fbc_fines.models import Fine
    
    current_borrowings = BookBorrowing.objects.filter(
        user=user, 
        status='active'
    ).select_related('book').order_by('-borrowed_date')
    
    pending_fines = Fine.objects.filter(
        user=user, 
        status='pending'
    ).order_by('-date_issued')
    
    # Mock recent activities (you can implement this based on your activity logging)
    recent_activities = [
        {
            'description': 'Logged into the system',
            'timestamp': user.last_activity or user.last_login,
            'icon': 'sign-in-alt'
        },
        # Add more activities based on your system's activity logging
    ]
    
    context = {
        'user': user,
        'current_borrowings': current_borrowings,
        'pending_fines': pending_fines,
        'recent_activities': recent_activities,
        'title': f'User Details - {user.get_full_name()}'
    }
    return render(request, 'users/user_details.html', context)

@login_required
@user_passes_test(is_admin_only)
def system_settings_view(request):
    message = None
    error = None
    settings_obj = None
    
    try:
        settings_obj, created = SystemSettings.objects.get_or_create(id=1)
        if created:
            print("Created new SystemSettings object")
        
        if request.method == 'POST':
            # Handle form submission
            system_name = request.POST.get('system_name', 'FBC Library System')
            primary_color = request.POST.get('primary_color', '#22c55e')
            sidebar_color = request.POST.get('sidebar_color', '#0f172a')
            header_color = request.POST.get('header_color', '#1e293b')
            footer_color = request.POST.get('footer_color', '#334155')
            
            # Update all fields
            settings_obj.system_name = system_name
            settings_obj.primary_color = primary_color
            settings_obj.sidebar_color = sidebar_color
            settings_obj.header_color = header_color
            settings_obj.footer_color = footer_color
            
            # Handle file uploads
            if 'logo' in request.FILES:
                settings_obj.logo = request.FILES['logo']
            
            if 'favicon' in request.FILES:
                settings_obj.favicon = request.FILES['favicon']
                
            settings_obj.save()
            message = 'System settings updated successfully.'
            
    except Exception as e:
        error = f"Error loading system settings: {str(e)}"
        print(f"SystemSettings error: {e}")  # Debug print
        
    context = {
        'settings': settings_obj,
        'message': message,
        'error': error,
        'title': 'System Settings',
        'user': request.user,  # Required by admin_base.html
        'system_name': getattr(settings_obj, 'system_name', 'FBC Library System') if settings_obj else 'FBC Library System',
    }
    
    print(f"Rendering template with context: settings={settings_obj}, error={error}")  # Debug print
    return render(request, 'dashboard/system_settings.html', context)


@login_required
def my_subscription(request):
    """Display user's subscription information"""
    if request.user.user_type != 'student':
        messages.error(request, 'Subscription is only available for students.')
        return redirect('fbc_users:student_dashboard')

    context = {
        'user': request.user,
        'title': 'My Subscription'
    }
    return render(request, 'users/my_subscription.html', context)


@login_required
def renew_subscription(request):
    """Display subscription renewal page with payment options"""
    if request.user.user_type != 'student':
        messages.error(request, 'Subscription is only available for students.')
        return redirect('fbc_users:student_dashboard')

    # For now, we'll just render the template.
    # In a real application, you would fetch subscription plans and prices here.
    context = {
        'title': 'Renew Subscription',
        'subscription_price': 500  # Example price
    }
    return render(request, 'users/renew_subscription.html', context)


@login_required
def process_subscription_payment(request):
    """Process the subscription payment"""
    if request.method != 'POST':
        return redirect('fbc_users:renew_subscription')

    payment_method = request.POST.get('payment_method')
    amount = 500  # Assuming a fixed subscription price for now
    payment_successful = False
    transaction_id = ""
    payment_details = {}

    if payment_method in ['orange_money', 'afrimoney', 'qmoney']:
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        # Simulate mobile money payment processing
        if phone_number and password: # Basic validation
            payment_successful = True
            transaction_id = f"MM-{timezone.now().timestamp()}"
            payment_details = {
                'payment_type': 'Mobile Money',
                'provider': payment_method,
                'phone_number': phone_number,
                'transaction_reference': transaction_id
            }
        else:
            messages.error(request, 'Please provide phone number and password for Mobile Money.')

    elif payment_method == 'paypal':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvc = request.POST.get('cvc')
        cardholder_name = request.POST.get('cardholder_name')
        # Simulate PayPal/Credit Card payment processing
        if card_number and expiry_date and cvc and cardholder_name: # Basic validation
            # In a real scenario, send these to a payment gateway (e.g., Stripe, PayPal API)
            # and get a token or confirmation. NEVER store raw card details.
            payment_successful = True
            transaction_id = f"CC-{timezone.now().timestamp()}"
            # Store only last 4 digits for reference
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number
            payment_details = {
                'payment_type': 'Credit Card',
                'last_four_digits': last_four,
                'expiry_date': expiry_date,
                'cardholder_name': cardholder_name,
                'transaction_reference': transaction_id
            }
        else:
            messages.error(request, 'Please provide all credit card details including cardholder name.')

    if payment_successful:
        user = request.user
        # Update user's subscription
        if user.subscription_end_date and user.subscription_end_date > timezone.now():
            user.subscription_end_date += timezone.timedelta(days=365)
        else:
            user.subscription_end_date = timezone.now() + timezone.timedelta(days=365)
        user.is_subscription_active = True
        user.save()

        # Record the payment
        Payment.objects.create(
            user=user,
            amount=amount,
            payment_type='subscription',
            payment_method=payment_method,
            transaction_id=transaction_id,
            status='completed',
            details=payment_details
        )
        messages.success(request, 'Your subscription has been successfully renewed!')
        return redirect('fbc_users:my_subscription')
    else:
        # If payment was not successful due to missing fields, messages are already set.
        # If there was a simulated payment gateway error, you'd set a message here.
        messages.error(request, 'Payment failed. Please check your details and try again.')
        return redirect('fbc_users:renew_subscription')
