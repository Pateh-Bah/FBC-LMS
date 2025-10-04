from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'fbc_users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lecturer-dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff-dashboard-beautiful/', views.staff_dashboard_beautiful, name='staff_dashboard_beautiful'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('my-subscription/', views.my_subscription, name='my_subscription'),
    path('renew-subscription/', views.renew_subscription, name='renew_subscription'),
    path('process-subscription-payment/', views.process_subscription_payment, name='process_subscription_payment'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url='/users/login/'
         ), 
         name='password_reset_confirm'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-users/add/', views.add_user, name='add_user'),
    path('manage-users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('manage-users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('manage-users/details/<int:user_id>/', views.user_details, name='user_details'),
    
    # Legacy URLs for backward compatibility
    path('manage/', views.manage_users, name='manage_users_legacy'),
    path('add/', views.add_user, name='add_user_legacy'),
    path('edit/<int:user_id>/', views.edit_user, name='edit_user_legacy'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user_legacy'),
    path('details/<int:user_id>/', views.user_details, name='user_details_legacy'),
    path('system-settings/', views.system_settings_view, name='system_settings'),
]
