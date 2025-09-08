import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def create_users():    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin@123'
        )
        admin_user.user_type = 'admin'
        admin_user.university_id = 'ADMIN001'
        admin_user.save()
        print('Admin user created successfully')
    else:
        print('Admin user already exists')

    # Create lecturer user
    lecturer = User.objects.filter(username='lecturer').first()
    if not lecturer:
        lecturer = User.objects.create_user(
            username='lecturer',
            email='lecturer@example.com',
            password='lecturer1',
            first_name='John',
            last_name='Doe',
            is_staff=True
        )
        lecturer.user_type = 'lecturer'
        lecturer.university_id = 'LEC001'
        lecturer.is_subscription_active = True  # Lecturers have permanent subscriptions
        lecturer.save()
        print('Lecturer user created successfully')
    else:
        print('Lecturer user already exists')

if __name__ == '__main__':
    create_users()
