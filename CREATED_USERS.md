# Created Admin and Staff Users

## Users Created

### 1. Admin User
- **Username**: `fbcadmin`
- **Password**: `1234`
- **Email**: `fbcadmin@fbc.com`
- **Full Name**: `FBC Admin`
- **User Type**: `admin`
- **Is Staff**: `True`
- **Is Superuser**: `True`

### 2. Staff User
- **Username**: `fbcstaff`
- **Password**: `1234`
- **Email**: `fbcstaff@fbc.com`
- **Full Name**: `FBC Staff`
- **User Type**: `staff`
- **Is Staff**: `True`
- **Is Superuser**: `False`

## Login Instructions

### Custom Login System
- **URL**: `http://127.0.0.1:8000/users/login/`
- **Admin Login**: `fbcadmin` / `1234` → Redirects to `/dashboard/admin/`
- **Staff Login**: `fbcstaff` / `1234` → Redirects to `/dashboard/`

### Django Admin
- **URL**: `http://127.0.0.1:8000/admin/`
- **Admin Login**: `fbcadmin` / `1234` → Full admin access
- **Staff Login**: `fbcstaff` / `1234` → Limited admin access (no superuser)

## User Permissions

### fbcadmin (Admin User)
- ✅ Access to custom admin dashboard
- ✅ Full Django admin access (superuser)
- ✅ Can manage all books, users, borrowings
- ✅ Can access all management features
- ✅ Can create/edit/delete any content

### fbcstaff (Staff User)
- ✅ Access to regular user dashboard
- ✅ Limited Django admin access (staff but not superuser)
- ✅ Can manage books and borrowings
- ⚠️ Limited user management capabilities
- ⚠️ Cannot access some superuser-only features

## Verification

Both users have been tested and verified:
- ✅ Authentication works correctly
- ✅ User types are properly set
- ✅ Permissions are correctly assigned
- ✅ Login redirects work as expected

## Security Notes

⚠️ **Important**: The password `1234` is very simple and should only be used for testing/development. In production, ensure users change to strong passwords.

## Testing the Users

You can test these users by:
1. Going to `http://127.0.0.1:8000/users/login/`
2. Logging in with either:
   - `fbcadmin` / `1234`
   - `fbcstaff` / `1234`
3. Verify the redirect behavior and access permissions

The users are ready to use!
