from django.db import models
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    PAYMENT_TYPES = (
        ("subscription", "Annual Subscription"),
        ("fine", "Late Return Fine"),
    )    PAYMENT_METHODS = (
        ("orange_money", "Orange Money"),
        ("afrimoney", "Afrimoney"),
        ("qmoney", "QMoney"),
        ("paypal", "PayPal"),
        ("bank", "Bank Transfer"),
    )

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments"
    )
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.payment_type} - {self.amount} {settings.CURRENCY}"

    def mark_as_completed(self):
        self.status = "completed"
        self.completed_at = timezone.now()

        if self.payment_type == "subscription":
            current_date = timezone.now().date()
            if (
                self.user.subscription_valid_until
                and self.user.subscription_valid_until > current_date
            ):
                self.user.subscription_valid_until += timezone.timedelta(days=365)
            else:
                self.user.subscription_valid_until = current_date + timezone.timedelta(
                    days=365
                )
            self.user.save()

        elif self.payment_type == "fine":
            related_borrowing = self.related_borrowing.first()
            if related_borrowing:
                related_borrowing.fine_paid = True
                related_borrowing.save()

        self.save()


class PaymentDetail(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="details"
    )
    borrowing = models.ForeignKey(
        "fbc_books.BookBorrowing",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment_details",
    )
    reference = models.CharField(max_length=100)
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"Payment Detail: {self.payment.transaction_id}"
