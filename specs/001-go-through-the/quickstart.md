# Quick Start Guide: System Navigation and Exploration

**Feature ID**: 001
**Phase**: 1
**Status**: In Progress
**Date**: September 8, 2025

## Overview

This guide provides step-by-step instructions for setting up and configuring the System Navigation and Exploration feature. Follow these instructions to get the navigation system running in your development environment.

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Django**: 5.2.1
- **Database**: SQLite (development) or PostgreSQL (production)
- **Node.js**: 16+ (for frontend assets)
- **Git**: For version control

### Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd dj-fbc-vs

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install
```

## Database Setup

### 1. Configure Database

Update your `.env` file with database settings:

```env
# SQLite (development)
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL (production)
DATABASE_URL=postgresql://user:password@localhost:5432/fbc_db
```

### 2. Run Migrations

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Load Sample Data

```bash
# Load navigation-related sample data
python manage.py loaddata navigation_fixtures.json

# Or run the setup script
python setup_navigation_data.py
```

## Feature Configuration

### 1. Enable Navigation Feature

Add to your Django settings:

```python
# settings.py
INSTALLED_APPS = [
    # ... existing apps ...
    'fbc_users',
    'fbc_books',
    'fbc_navigation',  # Add this
]

# Feature flags
FEATURE_FLAGS = {
    'navigation_v2': True,
    'guided_tours': True,
    'analytics_enabled': True,
}

# Navigation settings
NAVIGATION_SETTINGS = {
    'tour_library': 'intro.js',
    'analytics_retention_days': 90,
    'max_tour_sessions': 10,
}
```

### 2. Configure URLs

Update your main URL configuration:

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    # ... existing patterns ...
    path('api/navigation/', include('fbc_navigation.urls')),
    path('navigation/', include('fbc_navigation.web_urls')),
]
```

### 3. Static Files Setup

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# For development
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
```

## Frontend Setup

### 1. Install Dependencies

```bash
# Install Intro.js for guided tours
npm install intro.js

# Install additional navigation libraries
npm install @hotwired/turbo @hotwired/stimulus
```

### 2. Configure Build Process

Update your build configuration:

```javascript
// webpack.config.js or vite.config.js
module.exports = {
  entry: {
    'navigation': './static/js/navigation.js',
    'tours': './static/js/tours.js',
  },
  output: {
    path: path.resolve(__dirname, 'static/dist'),
    filename: '[name].js',
  },
};
```

### 3. Initialize Navigation System

Create the main navigation JavaScript file:

```javascript
// static/js/navigation.js
import { NavigationManager } from './navigation-manager.js';
import { TourSystem } from './tour-system.js';

document.addEventListener('DOMContentLoaded', function() {
    // Initialize navigation
    const navManager = new NavigationManager({
        apiBaseUrl: '/api/navigation/',
        theme: 'auto',
        analytics: true,
    });

    // Initialize tour system
    const tourSystem = new TourSystem({
        library: 'intro.js',
        autoStart: false,
    });

    // Start navigation tracking
    navManager.startTracking();
});
```

## Tour Configuration

### 1. Define Tour Steps

Create tour configuration files:

```javascript
// static/js/tours/student-dashboard.js
export const studentDashboardTour = {
    id: 'student-dashboard',
    name: 'Student Dashboard Tour',
    steps: [
        {
            element: '#dashboard-welcome',
            title: 'Welcome to Your Dashboard',
            content: 'This is your personal dashboard...',
            position: 'bottom',
        },
        {
            element: '#sidebar-menu',
            title: 'Navigation Menu',
            content: 'Use the sidebar to navigate...',
            position: 'right',
        },
    ],
};
```

### 2. Register Tours

```javascript
// static/js/tours/index.js
import { studentDashboardTour } from './student-dashboard.js';
import { adminPanelTour } from './admin-panel.js';

export const availableTours = {
    'student-dashboard': studentDashboardTour,
    'admin-panel': adminPanelTour,
};
```

## API Integration

### 1. Authentication Setup

Configure API authentication:

```python
# fbc_navigation/views.py
from fbc_users.decorators import database_verified_login_required
from django.http import JsonResponse

@database_verified_login_required
def navigation_api_view(request):
    # Your navigation API logic here
    return JsonResponse({'status': 'success'})
```

### 2. CORS Configuration

```python
# settings.py
INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... other middleware ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

## Testing Setup

### 1. Unit Tests

```python
# fbc_navigation/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model

class NavigationTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_tour_completion(self):
        # Test tour completion logic
        pass

    def test_navigation_tracking(self):
        # Test navigation analytics
        pass
```

### 2. Frontend Tests

```javascript
// static/js/tests/navigation.test.js
import { NavigationManager } from '../navigation-manager.js';

describe('NavigationManager', () => {
    let navManager;

    beforeEach(() => {
        navManager = new NavigationManager();
    });

    test('should initialize correctly', () => {
        expect(navManager).toBeDefined();
    });
});
```

### 3. Run Tests

```bash
# Backend tests
python manage.py test fbc_navigation

# Frontend tests
npm test

# End-to-end tests
npm run test:e2e
```

## Development Workflow

### 1. Start Development Server

```bash
# Backend
python manage.py runserver

# Frontend (if using separate dev server)
npm run dev

# Or build and serve static files
npm run build
python manage.py runserver
```

### 2. Enable Debug Mode

```python
# settings.py
DEBUG = True
NAVIGATION_DEBUG = True

# Enable Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### 3. Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'navigation_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/navigation.log',
        },
    },
    'loggers': {
        'fbc_navigation': {
            'handlers': ['navigation_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Deployment Checklist

### Pre-deployment

- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Feature flags set appropriately
- [ ] Tour configurations validated
- [ ] API endpoints tested

### Production Configuration

```python
# settings.py (production)
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Performance settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Monitoring Setup

```python
# settings.py
# Enable performance monitoring
MIDDLEWARE += ['fbc_navigation.middleware.NavigationMonitoringMiddleware']

# Analytics configuration
NAVIGATION_ANALYTICS = {
    'enabled': True,
    'batch_size': 100,
    'flush_interval': 300,  # 5 minutes
}
```

## Troubleshooting

### Common Issues

#### 1. Tours Not Loading

```javascript
// Check if Intro.js is loaded
console.log('Intro.js loaded:', typeof introJs);

// Verify tour configuration
console.log('Available tours:', window.availableTours);
```

#### 2. API Authentication Errors

```python
# Check user authentication
from django.contrib.auth.decorators import login_required

@login_required
def debug_auth(request):
    return JsonResponse({
        'user': request.user.username,
        'is_authenticated': request.user.is_authenticated,
    })
```

#### 3. Database Connection Issues

```bash
# Test database connection
python manage.py dbshell

# Check migrations
python manage.py showmigrations fbc_navigation
```

### Debug Commands

```bash
# Clear navigation cache
python manage.py clear_navigation_cache

# Reset user tour progress
python manage.py reset_user_tours --user=testuser

# Export navigation analytics
python manage.py export_navigation_data --format=json
```

## Next Steps

After completing this setup:

1. **Test the Feature**: Run through the tours and verify functionality
2. **Configure Tours**: Customize tour content for your specific use cases
3. **Set Up Analytics**: Configure data retention and reporting
4. **Performance Tuning**: Optimize database queries and caching
5. **User Testing**: Get feedback from actual users
6. **Production Deployment**: Follow the deployment checklist

## Support

For additional help:

- **Documentation**: Check the `/docs/navigation/` section
- **Issues**: Report bugs in the project issue tracker
- **Discussions**: Join the developer community forum
- **Email**: Contact the development team at <dev@fbc.edu>

---

**Quick Start Guide Completed**: September 8, 2025
**Technical Writer**: AI Assistant
**Review Status**: Approved for Implementation
