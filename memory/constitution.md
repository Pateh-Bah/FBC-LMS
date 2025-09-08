# FBC Library Management System Constitution

## Core Principles

### I. Role-Based Security First

Every feature must enforce strict role-based permissions: Admin full access, Staff limited to students/lecturers, Lecturer same view as student without subscription, Student requires active subscription for premium features. Server-side validation is authoritative.

### II. Database-Verified Authentication

All views must use `database_verified_login_required` decorator to ensure user exists in DB and is not suspended. Authentication failures redirect to login with appropriate messages.

### III. Test-First Development (NON-NEGOTIABLE)

TDD mandatory: Write tests first, ensure they fail, then implement. Red-Green-Refactor cycle strictly enforced. Use existing test scripts in root directory.

### IV. Integration Testing

Focus areas requiring integration tests: User CRUD operations, role permission checks, subscription gating, logout message handling, venv activation in scripts.

### V. Simplicity and Maintainability

Start simple, follow YAGNI principles. Use existing decorators and patterns. Keep code readable and well-documented.

## Additional Constraints

Technology stack: Django 5.2.1, Python 3.11+, Tailwind CSS, PostgreSQL/SQLite, AWS S3 for media.

Environment: Virtual environment mandatory, auto-activated via `setup.ps1` and `run.ps1`.

Security: CSRF protection on all forms, secure password handling with `set_password()`, session preservation on self-password change.

## Development Workflow

Code review requirements: All changes must pass existing tests, follow role rules, maintain single logout message.

Testing gates: CRUD smoke tests, permission checks, subscription gating verification.

Deployment: Use `run.ps1` for dev, `server.ps1` for prod with Gunicorn.

## Governance

Constitution supersedes all other practices. Amendments require documentation and approval.

All PRs/reviews must verify compliance with role rules and authentication patterns.

Use `SYSTEM_SPECIFICATION.md` for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-09-08 | **Last Amended**: 2025-09-08
