from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Import SystemSettings to make it available to Django
from .system_settings import SystemSettings


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    university_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_suspended = models.BooleanField(default=False)
    is_subscription_active = models.BooleanField(default=False)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Additional fields for attendance tracking
    last_library_entry = models.DateTimeField(null=True, blank=True)
    total_library_visits = models.IntegerField(default=0)

    def __str__(self):
        name = self.get_full_name().strip()
        if name:
            return f"{name} ({self.user_type})"
        return f"{self.username} ({self.user_type})"

    @property
    def subscription_status(self):
        if self.user_type in ['lecturer', 'admin', 'staff']:
            return True
        if not self.is_subscription_active:
            return False
        if self.subscription_end_date and self.subscription_end_date < timezone.now():
            self.is_subscription_active = False
            self.save()
            return False
        return True

    def record_library_entry(self):
        """Record when a user enters the physical library"""
        self.last_library_entry = timezone.now()
        self.total_library_visits += 1
        self.save()

    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.user_type == 'admin'

    def can_manage_books(self):
        """Check if user can manage books"""
        return self.user_type in ['admin', 'staff']
    
    def can_manage_fines(self):
        """Check if user can manage fines"""
        return self.user_type in ['admin', 'staff']
    
    def can_access_reports(self):
        """Check if user can access reports"""
        return self.user_type == 'admin'
    
    def can_access_ebooks(self):
        """Check if user can access e-books"""
        if self.user_type in ['admin', 'staff', 'lecturer']:
            return True
        return self.subscription_status

    @property
    def active_borrowings_count(self):
        """Get count of active borrowings"""
        from fbc_books.models import BookBorrowing
        return BookBorrowing.objects.filter(user=self, status='active').count()

    @property
    def pending_fines_count(self):
        """Get count of pending fines"""
        from fbc_fines.models import Fine
        return Fine.objects.filter(user=self, status='pending').count()

    @property
    def total_fines(self):
        """Get total amount of pending fines"""
        from fbc_fines.models import Fine
        from django.db.models import Sum
        total = Fine.objects.filter(user=self, status='pending').aggregate(Sum('amount'))['amount__sum']
        return total or 0

    @property
    def unread_notifications_count(self):
        """Get count of unread notifications"""
        from fbc_notifications.models import LibraryNotification
        return LibraryNotification.objects.filter(recipient=self, unread=True).count()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        permissions = [
            ("can_suspend_users", "Can suspend users"),
            ("can_manage_ebooks", "Can manage e-books"),
            ("can_view_reports", "Can view reports"),
            ("can_manage_payments", "Can manage payments"),
            ("can_view_attendance", "Can view attendance logs"),
        ]


@receiver(post_save, sender=CustomUser)
def set_user_permissions(sender, instance, created, **kwargs):
    """Set initial permissions based on user type"""
    if created:
        if instance.user_type == 'admin':
            instance.is_staff = True
            instance.is_subscription_active = True
        elif instance.user_type == 'staff':
            instance.is_staff = True
            instance.is_subscription_active = True
        elif instance.user_type == 'lecturer':
            instance.is_subscription_active = True
        instance.save()
