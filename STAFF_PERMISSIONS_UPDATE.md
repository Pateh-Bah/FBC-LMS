# Staff Permission Restrictions Update

## Overview
This update implements additional permission restrictions for staff users in the library management system to ensure proper access control between different user types.

## Changes Made

### 1. User Management Restrictions for Staff

**Staff users can now:**
- Add all user types EXCEPT admin users
- Edit all user types EXCEPT admin users  
- Delete all user types EXCEPT admin users
- View details of all users (including admin users)

**Staff users cannot:**
- Create new admin users
- Edit existing admin users
- Delete existing admin users
- Access system appearance/settings

### 2. Code Changes

#### Views Updated (`fbc_users/views.py`):

1. **Added permission helper functions:**
   - `can_add_user_type(request_user, target_user_type)` - Checks if user can add specific user types
   - `can_edit_user(request_user, target_user)` - Checks if user can edit specific users
   - `can_delete_user(request_user, target_user)` - Checks if user can delete specific users

2. **Updated view decorators:**
   - `add_user`: Changed from `@user_passes_test(is_admin_only)` to `@user_passes_test(is_staff_or_admin)`
   - `edit_user`: Changed from `@user_passes_test(is_admin_only)` to `@user_passes_test(is_staff_or_admin)`
   - `delete_user`: Changed from `@user_passes_test(is_admin_only)` to `@user_passes_test(is_staff_or_admin)`
   - `system_settings_view`: Updated to use `@user_passes_test(is_admin_only)` only

3. **Added permission checks in views:**
   - All CRUD operations now check user permissions before proceeding
   - Appropriate error messages are shown when permissions are denied
   - Form submissions are blocked for unauthorized operations

#### Templates Updated:

1. **`templates/users/add_user.html`:**
   - Staff users can now see staff option but not admin option in user type dropdown

2. **`templates/users/edit_user.html`:**
   - Added visual warning for staff users attempting to edit admin users
   - Form is disabled when staff users try to edit admin users
   - User type dropdown shows appropriate options based on current user permissions

3. **`templates/users/manage_users.html`:**
   - Updated "Add New Member" button to show for both admin and staff
   - Export functionality remains admin-only
   - Action buttons (edit/delete) are hidden for admin users when current user is staff
   - JavaScript delete function updated to work for both admin and staff users

4. **`templates/admin/admin_base.html`:**
   - System Settings menu section is now only visible to admin users
   - Mobile dropdown menu also hides system settings for staff users

### 3. Security Enhancements

- **Server-side validation:** All permission checks are enforced at the view level
- **Client-side restrictions:** UI elements are hidden/disabled appropriately
- **Form protection:** Forms include hidden fields to prevent unauthorized submissions
- **Error handling:** Clear error messages inform users of permission restrictions

### 4. User Experience Improvements

- **Visual indicators:** Admin user badges are prominently displayed
- **Contextual buttons:** Action buttons only appear when users have appropriate permissions
- **Informative messages:** Success and error messages guide users appropriately
- **Graceful degradation:** Staff users see relevant functionality without confusion

## Testing Recommendations

1. **Test as Admin User:**
   - Verify full CRUD operations work on all user types
   - Confirm access to system settings
   - Check that all menu items are visible

2. **Test as Staff User:**
   - Verify can create student, lecturer, and staff users
   - Verify cannot create admin users
   - Verify can edit/delete non-admin users
   - Verify cannot edit/delete admin users
   - Confirm system settings are not accessible
   - Verify appropriate error messages appear

3. **Test Edge Cases:**
   - Try direct URL access to restricted endpoints
   - Verify form submissions with manipulated data are blocked
   - Test permission changes work immediately

## Security Notes

- All restrictions are enforced server-side for security
- Client-side restrictions are for UX improvement only
- Permission checks occur at multiple levels (view decorators, form validation, template rendering)
- No sensitive data exposure in templates for unauthorized users

## Future Considerations

- Consider adding audit logging for permission-related actions
- May want to add more granular permissions for specific operations
- Could implement role-based permissions for more complex hierarchies
