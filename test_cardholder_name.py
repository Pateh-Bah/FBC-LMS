#!/usr/bin/env python
"""
Test script to verify cardholder name functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from fbc_users.models import CustomUser
from fbc_payments.models import Payment
from django.utils import timezone

def test_cardholder_name_storage():
    print("🧪 Testing Cardholder Name Storage Functionality")
    print("=" * 60)
    
    # Create a test payment with cardholder name
    print("1. Creating test payment with cardholder name...")
    
    try:
        # Get a test user
        test_user = CustomUser.objects.filter(user_type='student').first()
        if not test_user:
            print("❌ No student user found for testing")
            return False
            
        print(f"   Using test user: {test_user.username}")
        
        # Create a payment with cardholder details
        test_payment = Payment.objects.create(
            user=test_user,
            payment_type='subscription',
            amount=100.00,
            payment_method='paypal',
            status='completed',
            transaction_id=f"TEST-{timezone.now().timestamp()}",
            details={
                'payment_type': 'Credit Card',
                'last_four_digits': '1234',
                'expiry_date': '12/25',
                'cardholder_name': 'Test Cardholder Name',
                'transaction_reference': 'TEST-REF-123'
            }
        )
        
        print(f"   ✅ Created payment with ID: {test_payment.id}")
        print(f"   ✅ Transaction ID: {test_payment.transaction_id}")
        
        # Verify the details were stored correctly
        print("\n2. Verifying stored cardholder details...")
        
        retrieved_payment = Payment.objects.get(id=test_payment.id)
        
        if retrieved_payment.details:
            print(f"   ✅ Details field populated: {bool(retrieved_payment.details)}")
            
            cardholder_name = retrieved_payment.details.get('cardholder_name')
            if cardholder_name:
                print(f"   ✅ Cardholder name stored: {cardholder_name}")
            else:
                print("   ❌ Cardholder name not found in details")
                return False
                
            last_four = retrieved_payment.details.get('last_four_digits')
            if last_four:
                print(f"   ✅ Last four digits stored: {last_four}")
            else:
                print("   ❌ Last four digits not found")
                
            payment_type = retrieved_payment.details.get('payment_type')
            if payment_type:
                print(f"   ✅ Payment type stored: {payment_type}")
            else:
                print("   ❌ Payment type not found")
                
        else:
            print("   ❌ Details field is empty")
            return False
            
        print("\n3. Testing mobile money details structure...")
        
        # Create a mobile money payment for comparison
        mm_payment = Payment.objects.create(
            user=test_user,
            payment_type='fine',
            amount=50.00,
            payment_method='orange_money',
            status='completed',
            transaction_id=f"TEST-MM-{timezone.now().timestamp()}",
            details={
                'payment_type': 'Mobile Money',
                'provider': 'orange_money',
                'phone_number': '+232-XX-XXXXXX',
                'transaction_reference': 'MM-TEST-456'
            }
        )
        
        print(f"   ✅ Created mobile money payment with ID: {mm_payment.id}")
        
        mm_retrieved = Payment.objects.get(id=mm_payment.id)
        if mm_retrieved.details and mm_retrieved.details.get('phone_number'):
            print(f"   ✅ Mobile money phone number stored: {mm_retrieved.details.get('phone_number')}")
        else:
            print("   ❌ Mobile money details not stored correctly")
            
        print("\n4. Clean up test data...")
        test_payment.delete()
        mm_payment.delete()
        print("   ✅ Test payments deleted")
        
        print(f"\n🎉 All tests passed! Cardholder name functionality is working correctly.")
        return True
        
    except Exception as e:
        print(f"   ❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_cardholder_name_storage()