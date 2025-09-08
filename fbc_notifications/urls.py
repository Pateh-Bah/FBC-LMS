from django.urls import path
from . import views

app_name = 'fbc_notifications'

urlpatterns = [
    # User notification views
    path('', views.view_notifications, name='notifications'),
    path('mark-read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('unread-count/', views.get_unread_count, name='get_unread_count'),
    
    # Admin management views
    path('manage/', views.manage_notifications, name='manage_notifications'),
    path('add/', views.add_notification, name='add_notification'),
    path('edit/<int:notification_id>/', views.edit_notification, name='edit_notification'),
    path('delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('details/<int:notification_id>/', views.notification_details, name='notification_details'),
    path('admin-mark-read/<int:notification_id>/', views.mark_notification_as_read, name='admin_mark_as_read'),
]
