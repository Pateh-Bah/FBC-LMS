Vercel + Supabase Deployment Guide for FBC-LMS

Overview
--------
This guide explains how to connect your GitHub repository (FBC-LMS) to Vercel for hosting and use Supabase as the Postgres backend. It lists the environment variables you need, how to construct the DATABASE_URL for Supabase, and safe deployment steps.

IMPORTANT SECURITY NOTE
-----------------------
- Never commit secrets (database passwords, service_role keys, API keys) to the repository.
- Add sensitive values directly into Vercel's Environment Variables (Project Settings) or GitHub Secrets if using CI.

Supabase project details you provided
------------------------------------
- Supabase Project ID: vkpbbepkwqenegbkxxli
- Supabase DB host: db.vkpbbepkwqenegbkxxli.supabase.co
- Supabase DB port: 5432
- Database name: postgres
- DB username: postgres
- DB password (raw): Fbc-lms@2205
- Supabase base URL: https://vkpbbepkwqenegbkxxli.supabase.co

Constructing DATABASE_URL (percent-encode password)
---------------------------------------------------
Database URL format (recommended with SSL):

postgresql://<DB_USER>:<ENCODED_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>?sslmode=require

To percent-encode the password (example using Python):

python -c "import urllib.parse; print(urllib.parse.quote('Fbc-lms@2205', safe=''))"

The encoded password for your DB password "Fbc-lms@2205" is: Fbc-lms%402205

Therefore the exact DATABASE_URL you can use (DO NOT COMMIT this into the repo; paste into Vercel or GitHub Secrets):

postgresql://postgres:Fbc-lms%402205@db.vkpbbepkwqenegbkxxli.supabase.co:5432/postgres?sslmode=require

Environment variables to set
---------------------------
Set the following environment variables in Vercel (Production and Preview as appropriate):

- SECRET_KEY: (generate a secure Django secret key; see below to generate)
- DEBUG: False (set to True only for local development)
- DJANGO_SETTINGS_MODULE: library_system.settings_vercel
- DATABASE_URL: (see exact value above)
- SUPABASE_URL: https://vkpbbepkwqenegbkxxli.supabase.co
- SUPABASE_ANON_KEY: <get from Supabase dashboard>
- SUPABASE_SERVICE_ROLE_KEY: <get from Supabase dashboard; use only for server-side operations>
- ALLOWED_HOSTS: localhost,127.0.0.1,*.vercel.app,your-custom-domain.com
- ANNUAL_SUBSCRIPTION_FEE: 100000
- FINE_PER_DAY: 5000

Client-side / NEXT_PUBLIC_ variables (for frontend apps)
-------------------------------------------------------
If you have a frontend (for example Next.js) that needs to talk directly to Supabase from the browser, use `NEXT_PUBLIC_` environment variables so the values are available to client-side code.

- NEXT_PUBLIC_SUPABASE_URL (public): https://vkpbbepkwqenegbkxxli.supabase.co
- NEXT_PUBLIC_SUPABASE_ANON_KEY (public): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrcGJiZXBrd3FlbmVnYmt4eGxpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0Mjc2OTEsImV4cCI6MjA3NTAwMzY5MX0.VnGYd0ITYLET6FHGWZ5vebuoPs2WsrGkqLPy0C1FnIQ

Notes and caution:
- The `NEXT_PUBLIC` ANON key is intended for client-side usage and is safe to expose; it has the permissions of the Supabase anon role only. Do NOT use the Service Role key here.
- Keep `SUPABASE_SERVICE_ROLE_KEY` secret and only set it on the server (Django) side.

Set these values in Vercel (PowerShell CLI example):

```powershell
vercel env add NEXT_PUBLIC_SUPABASE_URL "https://vkpbbepkwqenegbkxxli.supabase.co" production
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY "<PASTE_ANON_KEY_HERE>" production
```

To push many variables at once (including the server-only `SUPABASE_SERVICE_ROLE_KEY`) you can use the helper script included in the repository at `scripts/push_vercel_env_from_dotenv.ps1`.

Usage (PowerShell):

```powershell
# 1. Login to Vercel
vercel login

# 2. From the project root run the script to push variables from your local .env to Vercel
.\scripts\push_vercel_env_from_dotenv.ps1 -Environment production

# The script will prompt you to confirm uploading sensitive variables such as SUPABASE_SERVICE_ROLE_KEY and DATABASE_URL.
```

Or add them via the Vercel Dashboard > Project Settings > Environment Variables.

Optional email / storage variables
---------------------------------
- EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS
- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME (if using S3)

Where to find Supabase keys
---------------------------
1. Open your Supabase project.
2. Go to Settings > API.
3. Copy the "anon" key (SUPABASE_ANON_KEY) for client-only operations.
4. Copy the Service Role key (SUPABASE_SERVICE_ROLE_KEY) for server side operations (keep this secret!).

Vercel: connect repository and add environment variables
-------------------------------------------------------
1. Sign in to Vercel and choose "New Project".
2. Import your GitHub repo (FBC-LMS).
3. For the "Root Directory" choose the repository root if the Django project is at root.
4. For Build & Output settings (recommended options):
   - Install Command: pip install -r requirements-vercel.txt
   - Build Command: python manage.py collectstatic --noinput
   - Output Directory: staticfiles
   - Environment: set to "Production" variables as shown above

Note on running Django on Vercel (and alternatives)
--------------------------------------------------
Vercel is optimized for serverless and frontend frameworks. It supports Docker-based deployments for full Django apps, but if you do not want to use Docker there are two practical approaches:

1) Use a hosting provider that supports persistent Python web processes (recommended if you are not using Docker):
  - Render (render.com), Railway (railway.app), Fly (fly.io), or Heroku are excellent choices and can run Gunicorn directly from your Git repo using a `Procfile` or a `render.yaml` manifest.
  - I added a `Procfile` and a `render.yaml` manifest to this repo to make deploying to Render or Heroku straightforward.

2) Use Vercel only for your frontend (Next.js/React) and host Django on Render/Railway/Heroku. Keep the frontend and backend separated; the frontend uses `NEXT_PUBLIC_SUPABASE_*` to talk to Supabase or calls your Django API hosted elsewhere.

3) Advanced: Convert Django into serverless functions for Vercel (requires substantial refactor and a WSGI-to-serverless adapter). Not recommended unless you want to invest in serverless migration.

Given you prefer not to use Docker, I updated the repo to include a `Procfile` and a `render.yaml` so you can deploy to Render or Heroku with minimal changes.

Sample Dockerfile (recommended for Vercel Docker deployment)
-----------------------------------------------------------
# Sample Dockerfile (copy to project root as Dockerfile)
# Use a small Python base
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements-vercel.txt ./requirements-vercel.txt
RUN pip install --upgrade pip && pip install -r requirements-vercel.txt

# Copy project
COPY . /app

# Collect static files
ENV DJANGO_SETTINGS_MODULE=library_system.settings_vercel
RUN python manage.py collectstatic --noinput

# Run migrations at container start (optional entrypoint can run them)
# Expose port
EXPOSE 8000

# Start server with Gunicorn
CMD ["gunicorn", "library_system.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

Running migrations & database setup
----------------------------------
Before your app can serve pages using Supabase Postgres, you must run Django migrations against the Supabase DB:

1. Locally or in a CI job where DATABASE_URL is set:
   - python manage.py makemigrations
   - python manage.py migrate
2. Create superuser:
   - python manage.py createsuperuser

Automating migrations in CI/GitHub Actions (optional)
-----------------------------------------------------
You can add a GitHub Action that runs on push to main and executes migrations (use GitHub Secrets to store DATABASE_URL and other secrets). Example task:

```yaml
name: Deploy and Migrate
on:
  push:
    branches: [ main ]
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install requirements
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-vercel.txt
      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          DJANGO_SETTINGS_MODULE: library_system.settings_vercel
        run: |
          python manage.py migrate --noinput
```

Generating a SECRET_KEY
-----------------------
Use this Python one-liner to generate a secure key:

python -c "import secrets; print(secrets.token_urlsafe())"

Local development (.env)
------------------------
Create a local `.env` (DO NOT commit) using the structure from `env.example`. Example minimal `.env` for local dev using your Supabase DB (copy and save as `.env.local`):

SECRET_KEY=<generate-and-paste-here>
DEBUG=True
DJANGO_SETTINGS_MODULE=library_system.settings
DATABASE_URL=postgresql://postgres:Fbc-lms%402205@db.vkpbbepkwqenegbkxxli.supabase.co:5432/postgres?sslmode=require
SUPABASE_URL=https://vkpbbepkwqenegbkxxli.supabase.co
SUPABASE_ANON_KEY=<paste-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<paste-service-role-key>
ALLOWED_HOSTS=localhost,127.0.0.1
ANNUAL_SUBSCRIPTION_FEE=100000
FINE_PER_DAY=5000

Final notes
-----------
- After adding environment variables to Vercel and connecting the repo, you can trigger a production deployment.
- For production, set DEBUG=False and ensure SECRET_KEY and SERVICE_ROLE_KEY values are stored securely in Vercel.
- If you want, I can:
  - Add a Dockerfile to the repo and create a Vercel-ready deployment configuration.
  - Create a GitHub Action to run migrations automatically on deploy.
  - Provide the exact Vercel CLI commands to add environment variables if you want to automate that step.

If you'd like, I can now:
- Create the Dockerfile in the repo and commit it.
- Create a GitHub Action workflow file to run migrations.
- Provide exact Vercel CLI commands to add the listed environment variables (you'll need to be logged in with the Vercel CLI).

