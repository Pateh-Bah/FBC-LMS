# Vercel Deployment Steps for Django LMS

## 🎯 Quick Start Guide

### Prerequisites
- ✅ Virtual environment activated
- ✅ Supabase project created
- ✅ Supabase database password ready

## Step 1: Environment Setup

### 1.1 Activate Virtual Environment
```bash
# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 1.2 Install Requirements
```bash
pip install -r requirements.txt
```

### 1.3 Setup Environment Variables
```bash
# Copy the local environment template
copy env.local .env

# Edit .env file and add your Supabase database password
# Replace [YOUR-PASSWORD] with your actual password
```

## Step 2: Database Setup

### 2.1 Get Your Supabase Database Password
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project (`vkpbbepkwqenegbkxxli`)
3. Go to **Settings** → **Database**
4. Copy your database password

### 2.2 Update Environment Variables
Edit your `.env` file and replace `[YOUR-PASSWORD]` with your actual password:

```bash
DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.vkpbbepkwqenegbkxxli.supabase.co:5432/postgres
```

### 2.3 Run Database Migrations
```bash
# Set environment variables
set DJANGO_SETTINGS_MODULE=library_system.settings_vercel

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 3: Test Locally

### 3.1 Test with Supabase
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` and test your application.

## Step 4: Deploy to Vercel

### 4.1 Install Vercel CLI
```bash
npm install -g vercel
```

### 4.2 Login to Vercel
```bash
vercel login
```

### 4.3 Deploy
```bash
vercel --prod
```

Follow the prompts:
- Link to existing project? **No**
- Project name: **fbc-lms** (or your preferred name)
- Directory: **./**
- Override settings: **No**

## Step 5: Set Environment Variables in Vercel

### 5.1 Go to Vercel Dashboard
1. Visit [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**

### 5.2 Add These Variables

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | `django-insecure-change-this-to-a-secure-secret-key-in-production-2024` |
| `DEBUG` | `False` |
| `DJANGO_SETTINGS_MODULE` | `library_system.settings_vercel` |
| `SUPABASE_URL` | `https://vkpbbepkwqenegbkxxli.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrcGJiZXBrd3FlbmVnYmt4eGxpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0Mjc2OTEsImV4cCI6MjA3NTAwMzY5MX0.VnGYd0ITYLET6FHGWZ5vebuoPs2WsrGkqLPy0C1FnIQ` |
| `DATABASE_URL` | `postgresql://postgres:YOUR_PASSWORD@db.vkpbbepkwqenegbkxxli.supabase.co:5432/postgres` |
| `ANNUAL_SUBSCRIPTION_FEE` | `100000` |
| `FINE_PER_DAY` | `5000` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,*.vercel.app,*.vercel.app.,vkpbbepkwqenegbkxxli.supabase.co` |

**⚠️ Important: Replace `YOUR_PASSWORD` with your actual Supabase database password!**

### 5.3 Redeploy
After adding environment variables, redeploy:
```bash
vercel --prod
```

## Step 6: Test Your Deployment

1. Visit your Vercel URL
2. Test all major functionality:
   - User registration/login
   - Book browsing
   - Admin panel
   - Database operations

## 🔧 Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   - Make sure all dependencies are in `requirements.txt`
   - Check that virtual environment is activated

2. **Database connection errors**
   - Verify `DATABASE_URL` is correct
   - Check Supabase project is active
   - Ensure password is correct

3. **Static files not loading**
   - Run `python manage.py collectstatic --noinput`
   - Check WhiteNoise configuration

4. **Environment variables not working**
   - Make sure they're set in Vercel dashboard
   - Redeploy after adding variables

### Debug Mode:
Set `DEBUG=True` temporarily to see detailed error messages.

## 📁 Files Created for You:

- ✅ `requirements.txt` - Updated with exact versions
- ✅ `vercel.env` - Environment variables template
- ✅ `env.local` - Local development environment
- ✅ `setup_vercel.py` - Automated setup script
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function handler
- ✅ `library_system/settings_vercel.py` - Production settings

## 🚀 Quick Commands:

```bash
# Setup everything automatically
python setup_vercel.py

# Manual setup
pip install -r requirements.txt
copy env.local .env
# Edit .env with your password
python manage.py migrate
python manage.py collectstatic --noinput
vercel --prod
```

## 🎉 Success!

Once deployed, your Django LMS will be available at your Vercel URL!

**Note**: Vercel has limitations with Django. For better performance, consider Railway or Render for production use.
