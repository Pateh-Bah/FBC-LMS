from django.db import models
from django.conf import settings
from django.utils import timezone


class LibraryNotification(models.Model):
    NOTIFICATION_TYPES = (
        ("due_soon", "Book Due Soon"),
        ("overdue", "Book Overdue"),
        ("new_book", "New Book Added"),
        ("status_change", "Book Status Change"),
        ("fine", "Fine Notification"),
        ("suspension", "Account Suspension"),
        ("system", "System Notification"),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="library_notifications",
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    related_book = models.ForeignKey(
        "fbc_books.Book",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    related_borrowing = models.ForeignKey(
        "fbc_books.BookBorrowing",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    unread = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient} - {self.get_notification_type_display()}"

    def mark_as_read(self):
        self.unread = False
        self.save()


class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="general_notifications",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
