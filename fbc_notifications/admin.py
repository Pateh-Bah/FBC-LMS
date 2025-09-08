from django.contrib import admin
from .models import LibraryNotification


@admin.register(LibraryNotification)
class LibraryNotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "notification_type", "created_at", "unread", "title")
    list_filter = ("notification_type", "unread", "created_at")
    search_fields = ("recipient__username", "title", "description")
    readonly_fields = ("created_at",)

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(unread=False)

    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(unread=True)

    mark_as_unread.short_description = "Mark selected notifications as unread"
