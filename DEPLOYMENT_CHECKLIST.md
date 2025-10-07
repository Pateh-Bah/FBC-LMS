# Deployment Checklist

If Vercel reports "No Production Deployment / Your Production Domain is not serving traffic", follow these steps:

1. Confirm that the repository is connected to Vercel and the Production Branch is `main`.
2. Ensure a recent commit is pushed to `main`. You can trigger a redeploy by pushing a small commit.
3. Check Vercel Deployments -> Latest deployment logs for build errors.
4. Required environment variables (set in Vercel Dashboard -> Project -> Settings -> Environment Variables):
   - `DJANGO_SETTINGS_MODULE=library_system.settings_vercel`
   - `SECRET_KEY` (Django secret key)
   - `DATABASE_URL` (Supabase connection string)
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `DEBUG=False`
5. Optionally configure automatic deployments from GitHub by adding `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID` as GitHub repository secrets. Then the included GitHub Action `deploy-to-vercel.yml` will run and call `vercel --prod` on push to `main`.
6. If the build fails due to dependencies, check that `requirements-vercel.txt` includes only packages that are supported by Vercel's Python runtime or provide a custom build step using `build.sh`.
7. If you previously committed secrets to the repository, rotate them immediately and remove them from git history. (See `SECURITY.md`)

Troubleshooting quick checklist:
- Open Vercel Dashboard -> Deployments and inspect the most recent production deployment. Look for any build or runtime errors.
- Visit `/__health` on your production domain to ensure the serverless function responds.
- Temporarily enable `DEBUG=True` in Vercel environment variables to see more detailed error messages (remember to disable later).
