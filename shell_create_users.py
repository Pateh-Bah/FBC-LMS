from fbc_users.models import CustomUser
from django.db import transaction

print('Creating users in database...')

# Create admin user
with transaction.atomic():
    try:
        CustomUser.objects.filter(username='fbcadmin').delete()
        print('Deleted existing fbcadmin')
    except Exception as e:
        print(f'No existing fbcadmin to delete: {e}')
    
    admin_user = CustomUser.objects.create_user(
        username='fbcadmin',
        email='fbcadmin@fbc.com',
        password='1234',
        first_name='FBC',
        last_name='Admin',
        user_type='admin',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    print(f'✅ Created fbcadmin with ID: {admin_user.id}')

# Create staff user  
with transaction.atomic():
    try:
        CustomUser.objects.filter(username='fbcstaff').delete()
        print('Deleted existing fbcstaff')
    except Exception as e:
        print(f'No existing fbcstaff to delete: {e}')
        
    staff_user = CustomUser.objects.create_user(
        username='fbcstaff',
        email='fbcstaff@fbc.com',
        password='1234',
        first_name='FBC',
        last_name='Staff',
        user_type='staff',
        is_staff=True,
        is_superuser=False,
        is_active=True
    )
    print(f'✅ Created fbcstaff with ID: {staff_user.id}')

print('\nVerifying users in database...')
for user in CustomUser.objects.filter(username__in=['fbcadmin', 'fbcstaff']):
    print(f'✅ {user.username}: ID={user.id}, Type={user.user_type}, Staff={user.is_staff}, Super={user.is_superuser}')

# Test authentication
from django.contrib.auth import authenticate

print('\nTesting authentication from database...')
admin_auth = authenticate(username='fbcadmin', password='1234')
if admin_auth:
    print('✅ fbcadmin authentication: SUCCESS')
else:
    print('❌ fbcadmin authentication: FAILED')
    
staff_auth = authenticate(username='fbcstaff', password='1234')
if staff_auth:
    print('✅ fbcstaff authentication: SUCCESS')
else:
    print('❌ fbcstaff authentication: FAILED')
    
print('\n✅ Users created successfully in SQLite database!')
print('Database location: db.sqlite3')
