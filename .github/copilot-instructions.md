# FBC Library Management System - AI Coding Guide

## Architecture Overview
This is a Django 5.2.1 library management system with a role-based architecture supporting students, lecturers, staff, and admin users. The system uses a modular app structure with strict user type enforcement and custom authentication decorators.

## Key Apps & Responsibilities
- **`fbc_users`**: Custom user model, authentication, role-based permissions, system settings
- **`fbc_books`**: Book catalog, borrowing system, e-book management, root URL handling  
- **`fbc_fines`**: Fine calculation, payment tracking, overdue management
- **`fbc_payments`**: Payment processing, subscription management
- **`fbc_notifications`**: In-app notification system

## Critical Authentication Patterns

### Custom User Model
```python
# fbc_users/models.py - CustomUser extends AbstractUser
USER_TYPE_CHOICES = ('student', 'lecturer', 'staff', 'admin')
# Key fields: user_type, university_id, is_suspended, subscription_end_date
```

### Security Decorators (fbc_users/decorators.py)
Always use these instead of Django's standard decorators:
- `@database_verified_login_required` - Ensures user exists in DB and isn't suspended
- `@user_type_required(['admin', 'staff'])` - Role-based access control
- `@admin_required` - Admin-only views
- `@staff_or_admin_required` - Staff/admin views
- `@active_subscription_required` - Premium features for students

### Permission Hierarchy
- **Admin**: Full CRUD on all users, system settings, reports
- **Staff**: Manage books, students, lecturers (cannot create admins)
- **Lecturer**: View access, automatic subscription
- **Student**: Basic access, requires paid subscription for e-books

## Development Workflow

### Environment Setup
```bash
# Activate virtual environment (Windows)
& "C:\path\to\venv\Scripts\Activate.ps1"

# Install dependencies
pip install -r requirements.txt

# Environment variables from .env file
SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL
ANNUAL_SUBSCRIPTION_FEE=100000, FINE_PER_DAY=5000
```

### One-Time Setup (venv-first)
```powershell
# From project root
./setup.ps1  # creates & activates .\venv, installs requirements
```

### Running the Application
```bash
# Development server (auto-activates .\venv)
./run.ps1 dev

# Production (Gunicorn)
./run.ps1
```

### Database Management
```bash
# Create admin user (use setup_admin_user.py for known password)
python setup_admin_user.py  # Creates admin:admin123

# Shell access
python manage.py shell -c "from fbc_users.models import CustomUser; print(CustomUser.objects.count())"
```

## Template Architecture

### Base Templates
- `templates/admin/admin_base.html` - Admin interface with FBC theming
- `templates/base.html` - Public pages
- Uses Tailwind CSS with custom FBC color scheme (`fbc-green-*`, `fbc-navy-*`)

### Template Context
- System settings injected via `fbc_users.context_processors.system_settings_context`
- Variables: `system_name`, `primary_color`, `system_logo`, etc.

## URL Patterns & Legacy Support
```python
# Main routing (library_system/urls.py)
path('users/', include('fbc_users.urls'))     # User management
path('fines/', include('fbc_fines.urls'))     # Fines system  
path('', include('fbc_books.urls'))           # Root - books/dashboard

# Legacy redirects for old admin URLs
path('admin/dashboard/', RedirectView.as_view(url='/dashboard/admin/'))
```

## Common Debugging Patterns

### Template Issues
- Check `TEMPLATES.DIRS` points to project-level templates folder
- Use `{% load admin_tags %}` for admin templates
- Templates expect `user` context variable for permission checks

### Authentication Debugging
```python
# Test user permissions directly
python manage.py shell -c "from fbc_users.models import CustomUser; u=CustomUser.objects.get(username='admin'); print(f'{u.user_type}, suspended: {u.is_suspended}')"
```

### DisallowedHost Errors
- Check `ALLOWED_HOSTS` in `.env` file (common issue)
- Format: `ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0`

## Data Model Relationships
- User → BookBorrowing (one-to-many) 
- Book → BookBorrowing (one-to-many)
- User → Fine (one-to-many)
- Book → Fine (one-to-many, nullable)
- BookBorrowing calculates fines automatically on return

## JavaScript & Frontend Patterns
- Forms use Fetch API with CSRF tokens
- Password validation with real-time strength indicators
- Toast notifications via `showNotification()` function
- AJAX responses should return JSON: `{'success': True, 'message': '...'}`

## Testing Infrastructure
- Test scripts in root directory (test_*.py)
- `test_add_user_page.py`, `test_detailed_error.py` for debugging
- Use `python test_view_direct.py` to test views without HTTP layer

## Configuration Management
- System settings stored in database via `fbc_users.system_settings.SystemSettings`
- Runtime configuration through admin interface at `/users/system-settings/`
- Theme colors, logos, system name configurable per deployment

## Role & Permission Rules (Critical)
- Admin: Full CRUD on all users and settings.
- Staff: Same manage-users view as admin but with restrictions:
	- Can add/edit/delete only `student` and `lecturer` users.
	- Can view `admin` and `staff` users but cannot edit/delete them.
- Lecturer: Same dashboard view as student; cannot subscribe like students.
- Student: Requires active subscription for premium features.

Server-side enforcement used in `fbc_users/views.py`:
- `can_add_user_type`: staff limited to `student`/`lecturer`.
- `can_edit_user`: staff can edit `student`/`lecturer` and themselves only.
- `can_delete_user`: staff can delete `student`/`lecturer` only.
- Subscription gate via `@active_subscription_required` lets lecturers through without purchase.

## Operational Notes
- Logout shows a single success message; duplicates are cleared before redirect.
- Staff dashboards expose user management UI but actions are still validated server-side.