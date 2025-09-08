from django.core.management.base import BaseCommand
from fbc_users.models import CustomUser
from fbc_books.models import Book
from fbc_fines.models import Fine
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample fines for testing'

    def handle(self, *args, **options):
        # Clear existing fines
        Fine.objects.all().delete()
        
        # Get test data
        users = CustomUser.objects.all()
        books = Book.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found!'))
            return
            
        # Create sample fines
        user1 = users.first()
        book1 = books.first() if books.exists() else None
        
        fine1 = Fine.objects.create(
            user=user1,
            book=book1,
            fine_type='overdue',
            amount=Decimal('15.00'),
            reason='Book returned 3 days late'
        )
        
        fine2 = Fine.objects.create(
            user=user1,
            book=None,
            fine_type='general',
            amount=Decimal('10.00'),
            reason='General library fine'
        )
        
        if users.count() > 1:
            user2 = users.all()[1]
            fine3 = Fine.objects.create(
                user=user2,
                book=book1,
                fine_type='damage',
                amount=Decimal('50.00'),
                reason='Coffee stain on book'
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {Fine.objects.count()} sample fines')
        )
        
        for fine in Fine.objects.all():
            self.stdout.write(f'Fine {fine.id}: {fine.user.username} - Le {fine.amount} ({fine.fine_type})')
