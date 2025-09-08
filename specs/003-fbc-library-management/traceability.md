# Traceability Matrix – Feature 003 FBC Library Management System

Status Legend: ✅ Implemented (verified), ⚠ Partial / needs validation, ❌ Missing, 💤 Deferred
Priority (for gaps): P0 = Must before release; P1 = Important; P2 = Nice-to-have / future.

## Functional Requirements

| ID | Requirement (Condensed) | Primary Module(s) | Current Status | Notes / Follow-up |
|----|-------------------------|-------------------|----------------|-------------------|
| REQ-AUTH-001 | Multi-role auth (student/lecturer/staff/admin) | `fbc_users` | ✅ | Custom user model + user_type field |
| REQ-AUTH-002 | Database-verified login & suspension check | `fbc_users` | ✅ | Decorator `database_verified_login_required` present |
| REQ-AUTH-003 | Role-based access enforcement | `fbc_users` | ✅ | Decorators for roles exist; need full coverage audit |
| REQ-AUTH-004 | Single logout success message | `fbc_users` | ⚠ | Behavior documented; confirm no duplicates |
| REQ-AUTH-005 | Session management + activity tracking | `fbc_users` | ❌ | last_activity field present; middleware not implemented (P0) |
| REQ-USER-001 | Admin full CRUD users | `fbc_users` | ⚠ | Likely present; verify staff restrictions logic |
| REQ-USER-002 | Staff restricted CRUD (student/lecturer only) | `fbc_users` | ✅ | Server-side checks referenced in docs |
| REQ-USER-003 | Lecturer auto access (no subscription) | `fbc_users` | ✅ | Subscription decorator bypass needed—verify code |
| REQ-USER-004 | Student subscription gate premium features | `fbc_users`,`fbc_books` | ⚠ | Need to verify decorator usage on e-book endpoints (P0) |
| REQ-USER-005 | Profile management incl. image | `fbc_users` | ⚠ | File field? Confirm form & upload path |
| REQ-BOOK-001 | Book catalog w/ metadata | `fbc_books` | ✅ | Models + sample scripts present |
| REQ-BOOK-002 | Physical + e-book support | `fbc_books` | ✅ | E-book file field indicated (verify) |
| REQ-BOOK-003 | Borrow/return workflow | `fbc_books` | ✅ | Borrowing model present; confirm return logic |
| REQ-BOOK-004 | Overdue detection & fine calc | `fbc_fines`,`fbc_books` | ⚠ | Fine calc scripts exist; need auto overdue job plan |
| REQ-BOOK-005 | Borrowing restrictions/limits | `fbc_books` | ⚠ | Test `test_borrowing_restrictions.py` exists; confirm enforcement scope |
| REQ-FIN-001 | Subscription mgmt + payment | `fbc_payments` | ⚠ | Payment scripts exist; confirm subscription link logic |
| REQ-FIN-002 | Fine calculation + tracking | `fbc_fines` | ✅ | Fine model + creation scripts |
| REQ-FIN-003 | Payment gateway integration | `fbc_payments` | 💤 | Likely stub/local only (P1) |
| REQ-FIN-004 | Financial reporting | `fbc_payments`,`fbc_fines` | ❌ | Reports not evident (P1) |
| REQ-FIN-005 | Refund processing | `fbc_payments` | 💤 | Future feature (P2) |
| REQ-NAV-001 | Role-based navigation menus | templates | ⚠ | Menus exist; central config missing (P1) |
| REQ-NAV-002 | Guided tours onboarding | (new) | ❌ | Not implemented (P0) |
| REQ-NAV-003 | System overview dashboard | templates | ⚠ | Dashboard exists—verify metrics coverage |
| REQ-NAV-004 | Mobile responsive design | templates | ⚠ | Needs accessibility/responsive audit |
| REQ-NAV-005 | Quick search | `fbc_books` | ⚠ | Search capability presence unknown |
| REQ-ADMIN-001 | System settings mgmt | `fbc_users` | ✅ | SystemSettings context processor exists |
| REQ-ADMIN-002 | Backup & restore | scripts | ❌ | Only manual DB present (P1) |
| REQ-ADMIN-003 | System monitoring/health | (new) | ❌ | Not implemented (P2) |
| REQ-ADMIN-004 | Log management | core | ⚠ | Basic logs; no UI or retention strategy |
| REQ-ADMIN-005 | External integrations (LDAP/SSO) | (new) | 💤 | Out of current scope (P2) |

## Non-Functional Requirements

| ID | Requirement | Area | Status | Notes |
|----|------------|------|--------|-------|
| PERF-001 | Page load <2s | full stack | ⚠ | Need baseline measurement (P1) |
| PERF-002 | 1000+ concurrent users | infra | 💤 | Load test not in place (P2) |
| PERF-003 | Query optimization | db | ⚠ | Need EXPLAIN review key queries |
| PERF-004 | CDN for static | deploy | 💤 | Future prod config (P2) |
| PERF-005 | Caching strategy | infra | ❌ | Not implemented (P1) |
| SEC-001 | OWASP compliance | security | ⚠ | Perform checklist audit |
| SEC-002 | CSRF protection | backend | ✅ | Django default + confirm templates |
| SEC-003 | Secure password handling | backend | ✅ | Django auth handles hashing |
| SEC-004 | Role permission enforcement | backend | ⚠ | Need systematic test coverage |
| SEC-005 | Audit logging | backend | ❌ | No dedicated audit log (P1) |
| USAB-001 | WCAG 2.1 AA | frontend | ❌ | Requires audit (P1) |
| USAB-002 | Mobile-first | frontend | ⚠ | Likely partial; test across viewports |
| USAB-003 | Intuitive navigation | UX | ⚠ | Pending guided tour + nav refactor |
| USAB-004 | Help docs | docs | ⚠ | Some markdown files; user-facing help minimal |
| USAB-005 | Multi-language prep | i18n | 💤 | Not started (P2) |
| REL-001 | 99.9% uptime | ops | 💤 | Requires monitoring + deployment strategy |
| REL-002 | Automated backup | ops | ❌ | No scripts (P1) |
| REL-003 | Graceful error handling | backend | ⚠ | Need custom 403/404/500 templates |
| REL-004 | Data integrity constraints | db | ✅ | Models define basics; verify constraints |
| REL-005 | Transaction rollback | db | ✅ | Django ORM transactions available |

## Derived Implementation Tasks (From Gaps)

| Gap | Priority | Proposed Action | Linked Epic |
|-----|----------|-----------------|------------|
| Session activity tracking missing | P0 | Middleware + last_activity updates | Auth Foundations |
| Guided tour system absent | P0 | Create models + endpoints + JS integration | Navigation & Tours |
| Subscription gating verification incomplete | P0 | Audit decorators on e-book/download views | Auth Foundations |
| Fine overdue automation not scheduled | P0 | Add management command placeholder | Circulation |
| Audit logging absent | P1 | Introduce audit_log table or structured logging config | Auth Foundations |
| Central nav config missing | P1 | Implement navigation service module | Navigation & Tours |
| Caching layer absent | P1 | Add per-view caching + Redis toggle | API Perf |
| Financial reporting missing | P1 | Aggregation queries + export endpoint | Finance |
| WCAG/accessibility unverified | P1 | A11y audit + template fixes | Polishing |
| Backup automation missing | P1 | Add backup script + doc | Polishing |
| Search capability uncertain | P1 | Add simple title/author search query param | Circulation |
| Performance baseline absent | P1 | Measure key endpoints, record metrics | API Perf |
| Overdue reservation feature deferred | P2 | Schedule after core tours | Circulation |
| Payment gateway external integration | P2 | Abstract provider adapter | Finance |
| Monitoring/health endpoints | P2 | Add /healthz and logging hooks | Polishing |
| Multi-language support | P2 | Add i18n scaffolding | Polishing |

## Next Steps

1. Validate status marks (convert ⚠ to ✅/❌ after code inspection)
2. Generate `api_contract.md` with detailed schemas
3. Implement high-priority P0 tasks in upcoming milestones ordering
4. Update this matrix as tasks complete

---
Generated: 2025-09-08
