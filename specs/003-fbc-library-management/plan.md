# Implementation Plan: FBC Library Management System (Feature 003)

Branch: `003-fbc-library-management`
Specification: `specs/003-fbc-library-management/spec.md`
Generated: 2025-09-08

## 0. Summary

This plan operationalizes the approved specification into executable phases with traceability, migration ordering, API contracts, testing scope, risks, and acceptance criteria for development readiness.

## 1. Scope & Objectives

- Deliver multi-role library management (Student, Lecturer, Staff, Admin)
- Implement secure auth + role enforcement, circulation workflows, fines + subscriptions, navigation + guided tours
- Provide scalable API layer and maintainable data model evolution

Out of Scope (Phase 3+): AI recommendations, full multi-language UI, real-time push notifications.

## 2. Requirement Traceability (High-Level)

| Requirement Block | Key IDs (examples) | Initial Implementation Area |
|-------------------|--------------------|-----------------------------|
| Auth & Roles | REQ-AUTH-001..005 | `fbc_users` decorators, middleware |
| User Mgmt | REQ-USER-001..005 | `fbc_users` views/forms |
| Circulation | REQ-BOOK-001..005 | `fbc_books` models/views |
| Finance | REQ-FIN-001..005 | `fbc_fines`, `fbc_payments` |
| Navigation/UX | REQ-NAV-001..005 | templates + new nav service |
| System Admin | REQ-ADMIN-001..005 | settings model + admin views |
| Performance | PERF-* | caching, indexes, query review |
| Security | SEC-* | hardening tasks |
| Usability | USAB-* | accessibility passes |
| Reliability | REL-* | backups, error handling |

A detailed matrix will be produced in `traceability.md` (not yet generated in this plan step).

## 3. Epics & Milestones

| Milestone | Epic(s) | Duration | Exit Criteria |
|-----------|---------|----------|---------------|
| M1 | Core Auth & User Foundations | 1.5 wks | Login + decorators enforced; role dashboards load |
| M2 | Circulation & Fines Engine | 2 wks | Borrow/return with fine calculation tested |
| M3 | Subscriptions & Payments | 1.5 wks | Subscription gating + payment records functional |
| M4 | Navigation & Guided Tours | 2 wks | Role-based menus + tour tracking working |
| M5 | API Hardening & Performance | 1 wk | API contract endpoints pass tests, perf baselines met |
| M6 | Polishing, Accessibility, Reliability | 1 wk | A11y audit pass, error handling, backup procedure validated |

## 4. Detailed Work Breakdown (Initial Slice)

### Epic: Core Auth & User Foundations (M1)

- Audit existing custom user model vs spec (profile image, last_activity, subscription_end_date) – adjust migrations if needed
- Confirm decorator coverage (database_verified_login_required, user_type_required, etc.) vs requirements; add missing checks (session timeout, audit logging)
- Implement session activity tracker (middleware) updating last_activity
- Add audit log model (if required) or integrate with existing logging approach
- Validate logout single-success-message invariant

### Epic: Circulation & Fines Engine (M2)

- Verify borrowing restrictions logic (max concurrent, lecturer extensions)
- Implement overdue detection cron/task placeholder (future Celery-ready abstraction)
- Integrate fine calculation per FINE_PER_DAY; ensure idempotent recalculation on return
- Add reservation placeholder (deferred flag if not in existing scope)

### Epic: Subscriptions & Payments (M3)

- Subscription purchase flow (student only) using existing payment abstraction
- Auto-access for lecturers (bypass subscription decorator)
- Payment history view normalization (fine vs subscription)
- Subscription expiry job (daily check)

### Epic: Navigation & Guided Tours (M4)

- Central navigation config service (python module that returns role menu objects)
- Implement tour tracking tables (if not present) + minimal REST endpoints
- Guided tour JS integration stub (Intro.js) with data attributes

### Epic: API Hardening & Performance (M5)

- Implement/confirm REST endpoints in `api_contract.md`
- Add pagination, filtering standards
- Add caching (low-hanging: frequently accessed book list)

### Epic: Polishing, Accessibility, Reliability (M6)

- WCAG lint pass on templates
- Error boundary templates (user-friendly 403/404/500)
- Backup/documentation script (SQLite export now, PostgreSQL strategy noted)
- Monitoring hooks placeholder (future integration)

## 5. Data Model & Migration Plan (Draft)

| Change | Type | Migration Order | Notes |
|--------|------|-----------------|-------|
| Add last_activity index | Index | Early (M1) | Speeds session tracking reporting |
| Add audit log table | New table | M1 | Optional if not using existing logging |
| Navigation analytics table | New table | M4 | For tour + UX metrics |
| Tour completion table | New table | M4 | Supports guided tours |
| Reservation table (optional) | New table | Deferred | Only if reservation becomes in-scope |

All additions are additive → no destructive change before M6.

## 6. API Contract (Outline – Full version in `api_contract.md`)

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| /api/auth/login/ | POST | Public | Obtain session |
| /api/auth/logout/ | POST | Auth | End session |
| /api/auth/user/ | GET | Auth | Current user profile |
| /api/books/ | GET | Auth | List books (filter, paginate) |
| /api/books/{id}/borrow/ | POST | Role Student/Lecturer | Borrow action |
| /api/books/{id}/return/ | POST | Role Staff/Admin or owner | Return action |
| /api/fines/ | GET | Auth | List current user fines |
| /api/fines/{id}/pay/ | POST | Student | Pay fine |
| /api/subscription/ | POST | Student | Purchase/renew |
| /api/navigation/tours/ | GET | Auth | List tours |
| /api/navigation/tours/{id}/start/ | POST | Auth | Start or resume tour |
| /api/navigation/analytics/track/ | POST | Auth | Event tracking |

Error Envelope: `{ "success": false, "error": { "code": "...", "message": "..." } }`.

## 7. Testing Strategy Mapping (Delta from Spec)

| Epic | Unit Focus | Integration | Acceptance | Security |
|------|------------|-------------|------------|----------|
| Auth | decorators, middleware | login→dashboard | multi-role flows | privilege escalation tests |
| Circulation | fine calc, borrowing rules | borrow→return→fine | user journey borrow | tamper with book IDs |
| Finance | subscription expiry logic | payment + subscription | student purchase | replay payment attempts |
| Navigation/Tours | menu builder | API + UI render | first-login tour | unauthorized tour access |
| API Perf | cache layer utils | load test baseline | response time <2s | rate limiting placeholders |
| Polishing | util helpers | error views | a11y keyboard traversal | n/a |

Coverage Targets: core logic modules ≥85%; overall ≥80%.

## 8. Risks & Mitigations (Actionable)

| Risk | Impact | Likelihood | Mitigation | Trigger Action |
|------|--------|------------|-----------|----------------|
| Auth gaps missed | Security breach | Medium | Early audit + test harness | Block release until fixed |
| Fine calc edge errors | Revenue leakage | Medium | Write deterministic calc tests | Hotfix with migration if schema issue |
| Tour feature creep | Delay core delivery | High | Scope gate: M4 only minimal | Defer extras to post-M6 |
| Performance regressions | Poor UX | Medium | Baseline early (M2) + watch | Optimize queries before M5 end |
| Payment inconsistency | Trust loss | Low | Atomic DB transactions | Manual reconciliation job |

## 9. Acceptance Gates

- End M1: All auth decorators mapped & enforced, role dashboards load without 500s
- End M2: Borrow→overdue fine simulation passes tests
- End M3: Subscription gating active; lecturers bypass; payments persist
- End M4: Tour tracking stored + role menus generated dynamically
- End M5: All API endpoints return contract-compliant JSON + perf baseline captured
- End M6: A11y pass, backups documented, risks re-reviewed

## 10. Sign-off Criteria

Ready to move to development when:

- Traceability matrix complete; all P0 items scheduled
- `api_contract.md`, `migrations.md`, `testing_map.md` created
- No unresolved critical risks
- Product owner approval recorded

---
Generated plan scaffold. Next automated artifacts: traceability, full API contract, migrations detail, testing map, risk actions.
