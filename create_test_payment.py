#!/usr/bin/env python
"""
Create a test payment with cardholder name for display testing
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_users.models import CustomUser
from fbc_payments.models import Payment
from django.utils import timezone

def create_test_payment():
    print("💳 Creating test payment with cardholder name for display testing")
    print("=" * 60)
    
    try:
        # Get a student user
        test_user = CustomUser.objects.filter(user_type='student').first()
        if not test_user:
            print("❌ No student user found")
            return False
            
        print(f"📝 Using user: {test_user.username} ({test_user.get_full_name()})")
        
        # Create a payment with cardholder details
        payment = Payment.objects.create(
            user=test_user,
            payment_type='subscription',
            amount=500.00,
            payment_method='paypal',
            status='completed',
            transaction_id=f"CC-{timezone.now().timestamp()}",
            details={
                'payment_type': 'Credit Card',
                'last_four_digits': '4242',
                'expiry_date': '12/26',
                'cardholder_name': 'John Doe Student',
                'transaction_reference': f"CC-{timezone.now().timestamp()}"
            },
            completed_at=timezone.now()
        )
        
        print(f"✅ Created payment:")
        print(f"   - ID: {payment.id}")
        print(f"   - Transaction ID: {payment.transaction_id}")
        print(f"   - Amount: Le {payment.amount}")
        print(f"   - Method: {payment.get_payment_method_display()}")
        print(f"   - Cardholder: {payment.details.get('cardholder_name')}")
        print(f"   - Card ending: **** {payment.details.get('last_four_digits')}")
        
        # Also create a mobile money payment for comparison
        mm_payment = Payment.objects.create(
            user=test_user,
            payment_type='fine',
            amount=25.00,
            payment_method='orange_money',
            status='completed',
            transaction_id=f"MM-{timezone.now().timestamp()}",
            details={
                'payment_type': 'Mobile Money',
                'provider': 'orange_money',
                'phone_number': '+232-76-123456',
                'transaction_reference': f"MM-{timezone.now().timestamp()}"
            },
            completed_at=timezone.now()
        )
        
        print(f"\n✅ Also created mobile money payment:")
        print(f"   - ID: {mm_payment.id}")
        print(f"   - Phone: {mm_payment.details.get('phone_number')}")
        
        print(f"\n🎯 Now you can view the payment history at:")
        print(f"   http://127.0.0.1:8000/payments/history/")
        print(f"   (Login as admin to see all payments)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test payment: {str(e)}")
        return False

if __name__ == "__main__":
    create_test_payment()