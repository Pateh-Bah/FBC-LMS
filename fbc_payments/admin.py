from django.contrib import admin
from .models import Payment, PaymentDetail


class PaymentDetailInline(admin.TabularInline):
    model = PaymentDetail
    extra = 0
    readonly_fields = ("reference", "details")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payment_type",
        "amount",
        "payment_method",
        "status",
        "created_at",
        "completed_at",
    )
    list_filter = ("payment_type", "payment_method", "status")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "transaction_id",
    )
    readonly_fields = ("created_at", "completed_at")
    inlines = [PaymentDetailInline]

    actions = ["mark_as_completed", "mark_as_failed"]

    def mark_as_completed(self, request, queryset):
        for payment in queryset.filter(status="pending"):
            payment.mark_as_completed()

    mark_as_completed.short_description = "Mark selected payments as completed"

    def mark_as_failed(self, request, queryset):
        queryset.filter(status="pending").update(status="failed")

    mark_as_failed.short_description = "Mark selected payments as failed"
