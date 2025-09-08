from django.contrib import admin
from .models import Book, Author, Category, BookBorrowing


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "isbn",
        "status",
        "book_type",
        "total_copies",
        "available_copies",
    )
    list_filter = ("status", "book_type", "category")
    search_fields = ("title", "isbn", "authors__name")
    filter_horizontal = ("authors",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(BookBorrowing)
class BookBorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "user",
        "borrowed_date",
        "due_date",
        "returned_date",
        "status",
        "fine_amount",
        "fine_paid",
    )
    list_filter = ("status", "fine_paid")
    search_fields = (
        "book__title",
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = ("borrowed_date", "fine_amount")

    actions = ["mark_as_returned", "mark_as_lost", "mark_as_damaged"]

    def mark_as_returned(self, request, queryset):
        for borrowing in queryset:
            borrowing.mark_as_returned()

    mark_as_returned.short_description = "Mark selected borrowings as returned"

    def mark_as_lost(self, request, queryset):
        for borrowing in queryset:
            borrowing.mark_as_returned("lost")

    mark_as_lost.short_description = "Mark selected borrowings as lost"

    def mark_as_damaged(self, request, queryset):
        for borrowing in queryset:
            borrowing.mark_as_returned("damaged")

    mark_as_damaged.short_description = "Mark selected borrowings as damaged"
