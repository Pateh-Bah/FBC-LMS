from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("borrowed", "Borrowed"),
        ("lost", "Lost"),
        ("damaged", "Damaged"),
    )

    TYPE_CHOICES = (
        ("physical", "Physical Book"),
        ("ebook", "E-Book"),
    )

    title = models.CharField(max_length=200)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    authors = models.ManyToManyField(Author, related_name="books")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="books"
    )
    description = models.TextField()
    table_of_contents = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="book_covers/", null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    book_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="physical"
    )
    pdf_file = models.FileField(upload_to="ebooks/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def update_status(self):
        if self.available_copies == 0:
            self.status = "borrowed"
        elif self.available_copies == self.total_copies:
            self.status = "available"
        self.save()

    @property
    def current_borrowings(self):
        """Get all current (active) borrowings for this book"""
        return self.borrowings.filter(status="active", returned_date__isnull=True)


class BookBorrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )
    borrowed_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("returned", "Returned"),
            ("overdue", "Overdue"),
            ("lost", "Lost"),
            ("damaged", "Damaged"),
        ],
        default="active",
    )

    def __str__(self):
        return f"{self.book.title} - {self.user.get_full_name()}"

    def calculate_fine(self):
        if self.returned_date and self.returned_date > self.due_date:
            days_overdue = (self.returned_date - self.due_date).days
            self.fine_amount = days_overdue * settings.FINE_PER_DAY
            self.save()
        elif not self.returned_date and timezone.now() > self.due_date:
            days_overdue = (timezone.now() - self.due_date).days
            self.fine_amount = days_overdue * settings.FINE_PER_DAY
            self.save()
        return self.fine_amount

    def mark_as_returned(self, condition="good"):
        self.returned_date = timezone.now()
        self.status = "returned"

        self.book.available_copies += 1
        self.book.update_status()

        if condition == "damaged":
            self.status = "damaged"
            self.book.status = "damaged"
            self.book.save()
        elif condition == "lost":
            self.status = "lost"
            self.book.status = "lost"
            self.book.save()

        self.calculate_fine()
        self.save()
