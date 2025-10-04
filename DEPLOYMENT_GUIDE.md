# Django LMS Deployment Guide - Vercel + Supabase

## Overview
This guide will help you deploy your Django Library Management System to Vercel and connect it to Supabase for database and storage.

## ⚠️ Important Limitations

**Vercel is not ideal for Django applications** because:
- Django is a traditional web framework that needs persistent server processes
- Vercel is designed for serverless functions with execution time limits
- You may experience cold starts and performance issues
- Some Django features may not work properly

**Recommended alternatives for Django:**
- Railway (most Django-friendly)
- Render
- DigitalOcean App Platform
- Heroku

## Prerequisites
- GitHub account with your Django project
- Vercel account
- Supabase account

## Step 1: Supabase Setup

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign up/Sign in with GitHub
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - Name: `fbc-lms`
   - Database Password: (choose a strong password)
   - Region: Choose closest to your users
6. Click "Create new project"

### 1.2 Get Database Connection Details
1. Go to Settings > Database
2. Copy the connection details:
   - Host
   - Database name
   - Username
   - Password
   - Port (usually 5432)

### 1.3 Create Database Tables
1. Go to the SQL Editor in Supabase
2. Run the following commands to create your Django tables:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom user table (if needed)
-- Note: Django will create most tables automatically when you run migrations
```

### 1.4 Get API Keys
1. Go to Settings > API
2. Copy:
   - Project URL
   - Anon/Public key
   - Service role key (keep this secret!)

## Step 2: Vercel Deployment

### 2.1 Install Vercel CLI
```bash
npm install -g vercel
```

### 2.2 Login to Vercel
```bash
vercel login
```

### 2.3 Deploy to Vercel
```bash
# In your project directory
vercel

# Follow the prompts:
# - Link to existing project? No
# - Project name: fbc-lms
# - Directory: ./
# - Override settings: No
```

### 2.4 Set Environment Variables in Vercel
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings > Environment Variables
4. Add the following variables:

```
SECRET_KEY=your-django-secret-key
DEBUG=False
DATABASE_URL=postgresql://username:password@host:port/database_name
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
ANNUAL_SUBSCRIPTION_FEE=100000
FINE_PER_DAY=5000
DJANGO_SETTINGS_MODULE=library_system.settings_vercel
```

### 2.5 Run Django Migrations
Since Vercel doesn't support persistent databases, you'll need to run migrations manually:

1. Connect to your Supabase database
2. Use a tool like pgAdmin or DBeaver
3. Run Django migrations manually or use a script

## Step 3: Alternative Deployment (Recommended)

### 3.1 Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" > "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect Django and set up the environment
6. Add environment variables in Railway dashboard
7. Connect your Supabase database

### 3.2 Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Configure build and start commands:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn library_system.wsgi:application`
6. Add environment variables
7. Deploy

## Step 4: Database Migration to Supabase

### 4.1 Export Current Data (if you have data)
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json
```

### 4.2 Update Settings for Supabase
The `settings_vercel.py` file is already configured for Supabase.

### 4.3 Run Migrations
```bash
# Set environment variables locally
export DATABASE_URL="postgresql://username:password@host:port/database_name"
export DJANGO_SETTINGS_MODULE="library_system.settings_vercel"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load data (if you exported it)
python manage.py loaddata data.json
```

## Step 5: Static Files and Media

### 5.1 Static Files
Static files are handled by WhiteNoise in the Vercel configuration.

### 5.2 Media Files
For production, consider using:
- Supabase Storage
- AWS S3
- Cloudinary

## Step 6: Testing

### 6.1 Test Locally with Supabase
```bash
# Set environment variables
export DATABASE_URL="postgresql://username:password@host:port/database_name"
export DJANGO_SETTINGS_MODULE="library_system.settings_vercel"

# Run server
python manage.py runserver
```

### 6.2 Test Production Deployment
1. Visit your Vercel URL
2. Test all major functionality
3. Check database connections
4. Verify static files are loading

## Troubleshooting

### Common Issues:
1. **Static files not loading**: Check WhiteNoise configuration
2. **Database connection errors**: Verify DATABASE_URL format
3. **Cold starts**: Normal with serverless, consider Railway/Render
4. **File uploads**: May need cloud storage for production

### Debug Mode:
Set `DEBUG=True` temporarily to see detailed error messages.

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS (automatic with Vercel)
- [ ] Secure database credentials
- [ ] Configure CORS if needed
- [ ] Set up proper email configuration
- [ ] Regular database backups

## Next Steps

1. Set up monitoring (Sentry for error tracking)
2. Configure domain name
3. Set up SSL certificates
4. Implement CI/CD pipeline
5. Set up database backups
6. Configure logging

## Support

If you encounter issues:
1. Check Vercel function logs
2. Check Supabase logs
3. Review Django logs
4. Test locally with production settings
