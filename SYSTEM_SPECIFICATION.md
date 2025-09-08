# FBC Library Management System — System Specification

## 1. Purpose

Provide a complete, role-based library management system for FBC with secure authentication, book circulation, fines, subscriptions, and admin/staff dashboards. The system enforces strict permissions by user type and supports both physical and e-book flows. Includes comprehensive navigation, guided tours, spec-kit development workflow, and advanced user experience features.

## 2. Roles and Permissions

- **Admin**
  - Full CRUD on all users
  - Manage system settings, reports, books, fines, payments
  - Access all dashboards and views
  - System-wide configuration and analytics
  - Complete navigation and feature access

- **Staff**
  - Shares manage-users UI with Admin but restricted actions
  - Can add/edit/delete only Student and Lecturer users
  - Can view Admin and Staff users but cannot edit/delete them
  - Manage books and fines
  - Limited system settings access
  - Guided tours for staff-specific features

- **Lecturer**
  - Same dashboard/view as Student
  - Cannot subscribe (not required for premium features)
  - Automatic access to all library features
  - Enhanced navigation for academic resources

- **Student**
  - Access student dashboard
  - Requires active subscription for premium features (e.g., e-books)
  - Guided tours for subscription and borrowing features
  - Progressive feature unlocking based on subscription status

**Server-side enforcement (fbc_users):**

- `can_add_user_type`: staff → student/lecturer only
- `can_edit_user`: staff → student/lecturer; self-edit permitted
- `can_delete_user`: staff → student/lecturer only
- `@active_subscription_required`: grants staff/lecturer/admin access, students need active subscription

## 3. Apps and Responsibilities

- **fbc_users**: custom user model, authentication, dashboards, system settings, role management
- **fbc_books**: catalog, borrow/return flows, root URLs and admin dashboard, e-book management
- **fbc_fines**: overdue detection, fine creation, status tracking, payment integration
- **fbc_payments**: subscription/payment processing, payment history, billing management
- **fbc_notifications**: in-app notifications, alert system, user communication

## 4. Authentication and Security

- **CustomUser** extends Django user with:
  - `user_type`, `university_id`, `is_suspended`, `subscription_end_date`
  - Enhanced security with database verification
  - Session management and activity tracking

- **Decorators:**
  - `database_verified_login_required` — verifies live DB presence and active/suspended state
  - `user_type_required([...])`, `admin_required`, `staff_or_admin_required`
  - `active_subscription_required` — bypass for staff/lecturers/admin; students must subscribe

- **Security Features:**
  - Single logout message enforcement (duplicates cleared)
  - Message clearing on login preserves logout notice
  - CSRF protection on all forms
  - Secure password handling with session preservation
  - Role-based access control throughout the system

## 5. Key Views and URLs (fbc_users)

- **Authentication:**
  - `/users/login/` — secure login with role detection
  - `/users/logout/` — logout with single success message
  - `/users/dashboard/` — role-based dashboard redirect

- **User Dashboards:**
  - `/users/student-dashboard/`, `/lecturer-dashboard/`
  - `/users/staff-dashboard[-beautiful]/`, `/admin-dashboard/`
  - Enhanced with navigation guides and feature tours

- **User Management:**
  - `/users/manage-users/` — list/view (admin + staff)
  - `/users/manage-users/add/` — add member (admin + staff with restrictions)
  - `/users/manage-users/edit/<id>/` — edit member (admin + staff with restrictions)
  - `/users/manage-users/delete/<id>/` — delete member (admin; staff only for student/lecturer)
  - `/users/manage-users/details/<id>/` — member details

- **System Administration:**
  - `/users/system-settings/` — admin-only system settings
  - Enhanced configuration with validation and feedback

## 6. Data Model (high-level)

- **User (CustomUser)**
  - user_type: `student|lecturer|staff|admin`
  - university_id, phone_number, profile_image
  - is_suspended, is_active, subscription_end_date, last_activity
  - Enhanced with navigation preferences and tour completion tracking

- **Book**
  - metadata, status `available|borrowed`, relations to borrowing records
  - Support for physical and e-book formats
  - Enhanced catalog with search and filtering

- **BookBorrowing**
  - user, book, borrowed_date, due_date, returned_date, status `active|returned`
  - computes overdue and fine generation on return
  - Enhanced with borrowing restrictions and notifications

- **Fine**
  - user, book (nullable), amount, status `pending|paid`, date_issued
  - Integrated payment processing and history tracking

- **Payment**
  - user, amount, status `pending|completed`, created_at
  - Subscription management and payment history

- **LibraryNotification**
  - recipient, notification_type, created_at, content
  - Enhanced alert system with user preferences

- **TourCompletion** (New)
  - user, tour_id, completed_at, completion_status
  - Tracks user progress through guided tours

- **NavigationAnalytics** (New)
  - user, page_visited, timestamp, session_id
  - Tracks user navigation patterns for optimization

## 7. Frontend

- **Framework:** Tailwind CSS with custom FBC color palette
- **Themes:**
  - Admin themed templates: `templates/admin/admin_base.html`
  - Public/base templates: `templates/base.html`
  - Enhanced with navigation components and tour overlays

- **Interactive Features:**
  - CSRF-protected Fetch forms with JSON responses `{success|status, message}`
  - Toast/notification helpers via `showNotification()`
  - Guided tours using Intro.js or Shepherd.js
  - Responsive navigation with mobile support
  - Breadcrumb navigation and quick access panels

- **User Experience:**
  - Role-based navigation menus
  - Contextual help tooltips
  - Progressive feature disclosure
  - Loading states and feedback indicators

## 8. Environment and Configuration

- **Environment Variables (.env):**
  - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`
  - `ANNUAL_SUBSCRIPTION_FEE`, `FINE_PER_DAY`
  - Enhanced with navigation and tour configuration

- **Storage/Media:** S3 via `django-storages` when configured
- **Settings Module:** `library_system.settings`
- **Development Tools:** Integrated spec-kit workflow for feature development

## 9. Development Workflow (Spec-Kit Integration)

- **Feature Development Process:**
  - Spec-kit workflow with structured phases (specify → plan → develop → test → release)
  - Git branching strategy for feature isolation
  - Comprehensive specification documentation

- **Development Tools:**
  - Feature specification templates
  - Automated testing and validation
  - Code quality enforcement
  - Documentation generation

- **Quality Assurance:**
  - Automated linting and formatting
  - Comprehensive test coverage
  - Code review processes
  - Continuous integration checks

## 10. Navigation and Exploration Features

### Global Navigation System

- **Role-based menus** with collapsible sidebar for desktop
- **Mobile-responsive** bottom navigation
- **Quick search functionality** across all system features
- **Breadcrumb navigation** with clickable path history

### Guided Tours System

- **Interactive walkthroughs** for new users
- **Role-specific tours:**
  - Student: Borrowing, Subscription, Profile management
  - Lecturer: Dashboard, Book search, Borrowing history
  - Staff: User management, Book management, Reports
  - Admin: System settings, Full feature overview
- **Tour management:** completion tracking, reset functionality, analytics

### System Overview Dashboard

- **Feature overview** with visual representation
- **System statistics:** user counts by role, active borrowings
- **Getting started guide** with feature introduction
- **Help documentation** with contextual links

## 11. Install/Run (Windows PowerShell)

- **One-time setup:**

  ```powershell
  ./setup.ps1
  ```

- **Development:**

  ```powershell
  ./run.ps1 dev
  ```

- **Production:**

  ```powershell
  ./run.ps1
  ```

- **Spec-kit workflow:**

  ```bash
  # Create new feature
  bash scripts/create-new-feature.sh --json "feature name"

  # Plan implementation
  bash scripts/plan.sh

  # Develop and test
  bash scripts/develop.sh
  bash scripts/test.sh

  # Release
  bash scripts/release.sh
  ```

- All scripts auto-activate `.\venv` when present

## 12. Operational Behavior

- **Authentication:** Single logout alert enforced by clearing message storage
- **Authorization:** Server-side validation for all role-based restrictions
- **User Experience:** Guided tours and navigation assistance for new users
- **Data Integrity:** Comprehensive validation and error handling
- **Performance:** Optimized queries and caching for responsive navigation
- **Security:** Role-based access control with audit trails

## 13. Testing Expectations

- **Unit Tests:** Individual component and function testing
- **Integration Tests:** End-to-end workflow validation
- **Role-based Testing:** Permission enforcement verification
- **UI/UX Testing:** Navigation and tour functionality
- **Performance Testing:** Load testing for concurrent users

- **Test Categories:**
  - Authentication and authorization flows
  - CRUD operations for all user types
  - Navigation and tour completion
  - Subscription and payment processing
  - System settings and configuration

- **Automated Testing:**
  - Root-level `test_*.py` helpers for view checks
  - Spec-kit integrated testing workflow
  - Continuous integration with test reporting

## 14. Acceptance Criteria

- **Functional Requirements:**
  - Role enforcement exactly as specified for Admin/Staff/Lecturer/Student
  - All user CRUD paths function with server-side validation
  - Navigation system works across all device sizes
  - Guided tours complete successfully for all user types
  - Subscription gating works correctly

- **Technical Requirements:**
  - venv-first scripts reliably start app from clean machine
  - Single logout message observed consistently
  - All navigation accessible via keyboard
  - Screen reader compatible interface
  - Cross-browser compatibility

- **Quality Requirements:**
  - Comprehensive test coverage (>80%)
  - Code quality standards met
  - Documentation complete and up-to-date
  - Performance benchmarks achieved

## 15. Non-Goals

- External SSO/OAuth beyond configured allauth defaults
- Complex reporting/analytics beyond current dashboards
- Third-party payment processors beyond integrated solutions
- Mobile native applications (web-responsive only)

## 16. Future Enhancements

- **Advanced Features:**
  - Bulk user operations with role-respecting guards
  - Audit trail for user management actions
  - Notification preferences and delivery channels
  - Advanced search with AI-powered recommendations

- **Technical Improvements:**
  - API development for mobile app integration
  - Real-time notifications and chat support
  - Advanced analytics and reporting dashboard
  - Machine learning for book recommendations

- **User Experience:**
  - Voice-guided tours and accessibility enhancements
  - Personalized navigation based on usage patterns
  - Multi-language support and internationalization
  - Progressive Web App (PWA) capabilities

## 17. Development Roadmap

### Phase 1: Core System (Current)

- ✅ Role-based authentication and authorization
- ✅ Basic CRUD operations for all user types
- ✅ Book circulation and fine management
- ✅ Subscription and payment processing
- ✅ System settings and configuration

### Phase 2: Enhanced Navigation (In Progress)

- 🔄 Global navigation system implementation
- 🔄 Guided tours for user onboarding
- 🔄 System overview dashboard
- 🔄 Mobile-responsive design optimization

### Phase 3: Advanced Features (Planned)

- 📋 API development for integrations
- 📋 Advanced analytics and reporting
- 📋 AI-powered recommendations
- 📋 Real-time notifications

### Phase 4: Optimization (Future)

- 📋 Performance optimization and scaling
- 📋 Advanced security features
- 📋 Multi-language support
- 📋 PWA capabilities

## 18. Support and Maintenance

- **Documentation:** Comprehensive system specifications in spec-kit format
- **Testing:** Automated test suites with continuous integration
- **Monitoring:** System health checks and performance monitoring
- **Backup:** Automated database backups and recovery procedures
- **Updates:** Regular security updates and feature enhancements

## 19. Compliance and Security

- **Data Protection:** GDPR compliance for user data handling
- **Security Standards:** OWASP security guidelines implementation
- **Access Control:** Role-based permissions with audit logging
- **Privacy:** User data minimization and consent management
- **Incident Response:** Security incident handling procedures
