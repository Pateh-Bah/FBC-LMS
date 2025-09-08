from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification


def is_admin_or_staff(user):
    return user.is_authenticated and user.user_type in ["admin", "staff"]


def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser


@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, "fbc_notifications/notifications.html", {"notifications": notifications})


@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.unread = False
    notification.save()
    return JsonResponse({"status": "success"})


@login_required
def mark_all_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(recipient=request.user, unread=True).update(
            is_read=True, unread=False
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})


@login_required
def get_unread_count(request):
    count = Notification.objects.filter(
        recipient=request.user, unread=True
    ).count()
    return JsonResponse({"count": count})


@login_required
@user_passes_test(is_staff_or_admin)
def manage_notifications(request):
    from datetime import date
    
    notifications = Notification.objects.all().order_by('-created_at')
    
    # Calculate statistics
    total_notifications = notifications.count()
    unread_count = notifications.filter(is_read=False).count()
    today_count = notifications.filter(created_at__date=date.today()).count()
    alert_count = notifications.filter(
        title__icontains='alert'
    ).count() or notifications.filter(
        message__icontains='urgent'
    ).count()
    
    context = {
        "notifications": notifications,
        "title": "Manage Notifications",
        "total_notifications": total_notifications,
        "unread_count": unread_count,
        "today_count": today_count,
        "alert_count": alert_count,
    }
    return render(request, "fbc_notifications/manage_notifications.html", context)


@login_required
@user_passes_test(is_staff_or_admin)
def add_notification(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        recipient = request.POST.get("recipient")

        Notification.objects.create(
            title=title, message=message, recipient_id=recipient
        )
        messages.success(request, "Notification added successfully!")
        return redirect("fbc_notifications:manage_notifications")
    
    # Get all users for the recipient dropdown
    users = User.objects.all().order_by('first_name', 'last_name', 'username')
    context = {
        'users': users,
        'title': 'Add New Notification'
    }
    return render(request, "fbc_notifications/add_notification.html", context)


@login_required
@user_passes_test(is_staff_or_admin)
def edit_notification(request, notification_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    notification = get_object_or_404(Notification, id=notification_id)
    
    if request.method == "POST":
        notification.title = request.POST.get("title")
        notification.message = request.POST.get("message")
        notification.recipient_id = request.POST.get("recipient")
        
        # Handle mark as read checkbox
        if request.POST.get("mark_as_read"):
            notification.is_read = True
            notification.unread = False
        
        notification.save()
        messages.success(request, "Notification updated successfully!")
        return redirect("fbc_notifications:manage_notifications")
    
    # Get all users for the recipient dropdown
    users = User.objects.all().order_by('first_name', 'last_name', 'username')
    context = {
        "notification": notification,
        "users": users,
        "title": "Edit Notification"
    }
    return render(request, "fbc_notifications/edit_notification.html", context)


@login_required
@user_passes_test(is_staff_or_admin)
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    if request.method == "POST":
        notification.delete()
        
        # Handle AJAX requests
        if request.headers.get('content-type') == 'application/json':
            return JsonResponse({"status": "success", "message": "Notification deleted successfully!"})
        
        messages.success(request, "Notification deleted successfully!")
        return redirect("fbc_notifications:manage_notifications")
    
    # If not POST, redirect back
    return redirect("fbc_notifications:manage_notifications")


@login_required
@user_passes_test(is_staff_or_admin)
def notification_details(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Get other notifications for the same recipient (excluding current one)
    related_notifications = Notification.objects.filter(
        recipient=notification.recipient
    ).exclude(id=notification_id).order_by('-created_at')[:5]
    
    context = {
        "notification": notification,
        "related_notifications": related_notifications,
        "title": f"Notification Details - {notification.title}"
    }
    return render(request, "fbc_notifications/notification_details.html", context)


@login_required
def mark_notification_as_read(request, notification_id):
    """Mark a specific notification as read (for admin use)"""
    if request.method == "POST":
        notification = get_object_or_404(Notification, id=notification_id)
        notification.is_read = True
        notification.unread = False
        notification.save()
        
        # Handle AJAX requests
        if request.headers.get('content-type') == 'application/json':
            return JsonResponse({"status": "success", "message": "Notification marked as read!"})
        
        messages.success(request, "Notification marked as read!")
        return redirect("fbc_notifications:notification_details", notification_id=notification_id)
    
    return redirect("fbc_notifications:manage_notifications")
