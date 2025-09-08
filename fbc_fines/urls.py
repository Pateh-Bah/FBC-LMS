from django.urls import path
from . import views

app_name = 'fbc_fines'

urlpatterns = [
    path('', views.fine_list, name='fine_list'),
    path('my-fines/', views.my_fines, name='my_fines'),
    path('create/', views.create_fine, name='create_fine'),
    path('<int:pk>/', views.fine_detail, name='fine_detail'),
    path('<int:pk>/pay/', views.pay_fine, name='pay_fine'),
    path('<int:pk>/verify/', views.verify_payment, name='verify_payment'),
    path('manage/', views.manage_fines, name='manage_fines'),
    path('add/', views.add_fine, name='add_fine'),
    path('edit/<int:fine_id>/', views.edit_fine, name='edit_fine'),
    path('delete/<int:fine_id>/', views.delete_fine, name='delete_fine'),
    path('details/<int:fine_id>/', views.fine_details, name='fine_details'),
    # AJAX endpoints
    path('mark-paid/<int:fine_id>/', views.mark_fine_paid, name='mark_fine_paid'),
    path('ajax-delete/<int:fine_id>/', views.delete_fine, name='ajax_delete_fine'),
    path('export/', views.export_fines, name='export_fines'),
]