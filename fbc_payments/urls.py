from django.urls import path
from . import views

app_name = 'fbc_payments'

urlpatterns = [
    path('', views.my_payments, name='my_payments'),  # List payments (Read)
    path('initiate/', views.process_payment, name='process_payment'),  # Create payment
    path('simulate/', views.simulate_payment_form, name='simulate_payment_form'),
    path('complete/', views.complete_simulated_payment, name='complete_simulated_payment'),
    path('payment/<int:payment_id>/', views.payment_details, name='payment_detail'),  # Read specific payment
    path('history/', views.payment_history, name='payment_history'),  # Payment history for admin
    # Note: Payments are typically not deleted, only viewed and created
]
