from django import forms
from .models import Fine

class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ['fine_type', 'amount', 'book', 'due_date', 'notes']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class FinePaymentForm(forms.Form):
    PAYMENT_METHODS = (
        ('paypal', 'PayPal'),
        ('orange_money', 'Orange Money'),
        ('afri_money', 'Afri Money'),
        ('qmoney', 'QMoney'),
    )
    
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS)
    payment_reference = forms.CharField(required=False, help_text='Enter the transaction reference if available')
