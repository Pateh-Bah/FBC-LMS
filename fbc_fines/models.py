from django.db import models
from django.conf import settings
from fbc_books.models import Book
from decimal import Decimal

class Fine(models.Model):
    FINE_TYPE_CHOICES = (
        ('overdue', 'Overdue Book'),
        ('damage', 'Book Damage'),
        ('lost', 'Lost Book'),
        ('general', 'General Fine'),
        ('other', 'Other'),
    )

    FINE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    fine_type = models.CharField(max_length=10, choices=FINE_TYPE_CHOICES, default='general')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=FINE_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_fine_type_display()} fine for {self.user.username} - {self.amount}"

    class Meta:
        ordering = ['-date_issued']
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('fbc_fines:fine_detail', args=[str(self.id)])
