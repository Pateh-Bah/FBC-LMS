from django.contrib import admin
from .models import Fine

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'fine_type', 'amount', 'status', 'date_issued', 'due_date')
    list_filter = ('status', 'fine_type', 'date_issued')
    search_fields = ('user__username', 'book__title', 'payment_reference')
    readonly_fields = ('date_issued',)
    raw_id_fields = ('user', 'book')
    
    fieldsets = (
        ('Fine Details', {
            'fields': ('user', 'book', 'fine_type', 'amount', 'status')
        }),
        ('Dates', {
            'fields': ('date_issued', 'due_date')
        }),        ('Payment Information', {
            'fields': ('payment_date', 'payment_method', 'payment_reference')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )