# Navigation API Contracts

**Feature ID**: 001
**Phase**: 1
**Status**: In Progress
**Date**: September 8, 2025

## Overview

This document defines the API contracts for the System Navigation and Exploration feature. All endpoints follow RESTful conventions and include proper authentication, validation, and error handling.

## Authentication Requirements

All navigation endpoints require authentication using the existing `@database_verified_login_required` decorator. Additional role-based access may apply based on the endpoint.

### Headers

```http
Authorization: Bearer <token>
Content-Type: application/json
X-CSRFToken: <csrf_token>  # For POST/PUT/DELETE requests
```

### Response Format

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message",
  "timestamp": "2025-09-08T21:30:00Z"
}
```

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": { ... }
  },
  "timestamp": "2025-09-08T21:30:00Z"
}
```

## Tour Management Endpoints

### GET /api/navigation/tours/

Get available tours for the current user based on their role and completion status.

**Authentication**: Required
**Method**: GET
**Rate Limit**: 100 requests/minute

#### Request

```http
GET /api/navigation/tours/?status=available&role=student
```

**Query Parameters:**

- `status` (optional): `available`, `completed`, `in_progress`
- `role` (optional): Filter by user role
- `category` (optional): `onboarding`, `feature`, `advanced`

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "tours": [
      {
        "id": "student-dashboard",
        "title": "Student Dashboard Tour",
        "description": "Learn how to navigate your student dashboard",
        "category": "onboarding",
        "estimated_duration": 180,
        "steps_count": 8,
        "status": "available",
        "prerequisites": [],
        "tags": ["dashboard", "navigation", "student"]
      }
    ],
    "total_count": 1,
    "available_count": 1,
    "completed_count": 0
  }
}
```

#### Error Responses

- `401 Unauthorized`: User not authenticated
- `403 Forbidden`: User role not allowed to access tours

---

### POST /api/navigation/tours/{tour_id}/start/

Start a guided tour for the current user.

**Authentication**: Required
**Method**: POST
**Rate Limit**: 10 requests/minute

#### Request

```http
POST /api/navigation/tours/student-dashboard/start/
Content-Type: application/json

{
  "start_step": 1,
  "context": {
    "referrer": "dashboard",
    "user_agent": "Mozilla/5.0..."
  }
}
```

#### Response (201 Created)

```json
{
  "success": true,
  "data": {
    "tour_session": {
      "id": "session_12345",
      "tour_id": "student-dashboard",
      "user_id": 123,
      "current_step": 1,
      "total_steps": 8,
      "started_at": "2025-09-08T21:30:00Z",
      "status": "in_progress"
    },
    "next_step": {
      "step_number": 1,
      "title": "Welcome to Your Dashboard",
      "content": "This is your personal dashboard...",
      "target_element": "#dashboard-welcome",
      "position": "bottom"
    }
  }
}
```

#### Error Responses

- `400 Bad Request`: Tour already in progress or prerequisites not met
- `404 Not Found`: Tour not found or not available to user

---

### POST /api/navigation/tours/{tour_id}/step/

Advance to the next step in the tour or mark current step as completed.

**Authentication**: Required
**Method**: POST
**Rate Limit**: 30 requests/minute

#### Request

```http
POST /api/navigation/tours/student-dashboard/step/
Content-Type: application/json

{
  "action": "next",
  "current_step": 1,
  "interaction_data": {
    "time_spent": 15,
    "clicked_element": "#next-button",
    "user_feedback": "helpful"
  }
}
```

**Actions:**

- `next`: Move to next step
- `previous`: Go back to previous step
- `skip`: Skip current step
- `complete`: Mark tour as completed

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "tour_session": {
      "current_step": 2,
      "status": "in_progress",
      "progress_percentage": 25
    },
    "next_step": {
      "step_number": 2,
      "title": "Navigation Menu",
      "content": "Use the sidebar to navigate between sections...",
      "target_element": "#sidebar-menu",
      "position": "right"
    }
  }
}
```

---

### POST /api/navigation/tours/{tour_id}/complete/

Mark a tour as completed for the current user.

**Authentication**: Required
**Method**: POST
**Rate Limit**: 10 requests/minute

#### Request

```http
POST /api/navigation/tours/student-dashboard/complete/
Content-Type: application/json

{
  "completion_status": "completed",
  "feedback": {
    "rating": 5,
    "comments": "Very helpful tour!",
    "would_recommend": true
  }
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "completion_record": {
      "id": 456,
      "tour_id": "student-dashboard",
      "user_id": 123,
      "completed_at": "2025-09-08T21:45:00Z",
      "completion_status": "completed",
      "tour_version": "1.0",
      "total_time_spent": 180
    },
    "user_stats": {
      "tours_completed": 1,
      "total_tours_available": 5,
      "completion_rate": 20
    }
  }
}
```

## Navigation Analytics Endpoints

### POST /api/navigation/analytics/track/

Track user navigation events and interactions.

**Authentication**: Required
**Method**: POST
**Rate Limit**: 100 requests/minute

#### Request

```http
POST /api/navigation/analytics/track/
Content-Type: application/json

{
  "event_type": "page_view",
  "page_url": "/users/student-dashboard/",
  "referrer": "/users/login/",
  "interaction_type": "navigation",
  "element_clicked": "#borrow-book-btn",
  "time_spent": 45,
  "device_info": {
    "type": "desktop",
    "screen_resolution": "1920x1080",
    "user_agent": "Mozilla/5.0..."
  },
  "session_id": "session_abc123",
  "context": {
    "user_role": "student",
    "current_tour": null,
    "feature_flags": ["navigation_v2", "analytics_enabled"]
  }
}
```

#### Response (201 Created)

```json
{
  "success": true,
  "data": {
    "event_id": 789,
    "recorded_at": "2025-09-08T21:30:00Z",
    "session_continued": true
  }
}
```

---

### GET /api/navigation/analytics/user-activity/

Get user's navigation activity and analytics summary.

**Authentication**: Required (user can only access their own data)
**Method**: GET
**Rate Limit**: 30 requests/minute

#### Request

```http
GET /api/navigation/analytics/user-activity/?period=30d&group_by=day
```

**Query Parameters:**

- `period` (optional): `7d`, `30d`, `90d` (default: 30d)
- `group_by` (optional): `day`, `week`, `month`
- `event_type` (optional): Filter by event type

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "summary": {
      "total_sessions": 15,
      "total_page_views": 127,
      "avg_session_duration": 420,
      "most_visited_page": "/users/student-dashboard/",
      "tours_completed": 2,
      "tours_started": 3
    },
    "activity_timeline": [
      {
        "date": "2025-09-08",
        "page_views": 12,
        "unique_pages": 5,
        "session_duration": 380,
        "tours_interacted": 1
      }
    ],
    "popular_features": [
      {
        "feature": "book_search",
        "usage_count": 25,
        "last_used": "2025-09-08T21:30:00Z"
      }
    ]
  }
}
```

## User Preferences Endpoints

### GET /api/navigation/preferences/

Get current user's navigation preferences.

**Authentication**: Required
**Method**: GET
**Rate Limit**: 60 requests/minute

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "preferences": {
      "theme_preference": "auto",
      "navigation_style": "sidebar",
      "tour_enabled": true,
      "analytics_enabled": true,
      "reduced_motion": false,
      "font_size": "medium",
      "language_preference": "en",
      "auto_show_tours": true,
      "keyboard_shortcuts": true
    },
    "last_updated": "2025-09-08T20:00:00Z"
  }
}
```

---

### PUT /api/navigation/preferences/

Update user's navigation preferences.

**Authentication**: Required
**Method**: PUT
**Rate Limit**: 20 requests/minute

#### Request

```http
PUT /api/navigation/preferences/
Content-Type: application/json

{
  "theme_preference": "dark",
  "navigation_style": "sidebar",
  "tour_enabled": true,
  "analytics_enabled": false,
  "reduced_motion": false,
  "font_size": "large",
  "language_preference": "en"
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "preferences": {
      "theme_preference": "dark",
      "navigation_style": "sidebar",
      "tour_enabled": true,
      "analytics_enabled": false,
      "reduced_motion": false,
      "font_size": "large",
      "language_preference": "en",
      "last_updated": "2025-09-08T21:35:00Z"
    },
    "changes_applied": ["theme_preference", "analytics_enabled", "font_size"]
  }
}
```

## System Overview Endpoints

### GET /api/navigation/system-overview/

Get system overview and navigation structure for the current user.

**Authentication**: Required
**Method**: GET
**Rate Limit**: 30 requests/minute

#### Request

```http
GET /api/navigation/system-overview/?include_permissions=true
```

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "user_info": {
      "role": "student",
      "permissions": ["read_books", "borrow_books", "view_profile"],
      "subscription_status": "active",
      "last_login": "2025-09-08T09:00:00Z"
    },
    "navigation_structure": {
      "main_sections": [
        {
          "id": "dashboard",
          "title": "Dashboard",
          "url": "/users/student-dashboard/",
          "icon": "dashboard",
          "badge_count": 3,
          "is_active": true
        },
        {
          "id": "books",
          "title": "Book Catalog",
          "url": "/books/",
          "icon": "book",
          "children": [
            {
              "id": "search",
              "title": "Search Books",
              "url": "/books/search/"
            },
            {
              "id": "borrowed",
              "title": "My Borrowed Books",
              "url": "/books/borrowed/"
            }
          ]
        }
      ],
      "quick_actions": [
        {
          "id": "quick_search",
          "title": "Quick Search",
          "action": "open_search_modal",
          "shortcut": "Ctrl+K"
        }
      ]
    },
    "system_status": {
      "maintenance_mode": false,
      "new_features_available": true,
      "last_updated": "2025-09-08T21:00:00Z"
    }
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `NAV_001` | 400 | Invalid tour ID or tour not available |
| `NAV_002` | 400 | Tour already in progress |
| `NAV_003` | 400 | Prerequisites not met for tour |
| `NAV_004` | 403 | Insufficient permissions for tour |
| `NAV_005` | 404 | Tour not found |
| `NAV_006` | 429 | Rate limit exceeded |
| `NAV_007` | 400 | Invalid preference value |
| `NAV_008` | 500 | Analytics tracking failed |

## Rate Limiting

- **Tour Management**: 10 requests/minute per user
- **Analytics Tracking**: 100 requests/minute per user
- **Preferences**: 20 requests/minute per user
- **System Overview**: 30 requests/minute per user

Rate limits are enforced per user and reset every minute. Exceeding limits returns HTTP 429 with retry information.

## Versioning

API endpoints support versioning through Accept headers:

```http
Accept: application/vnd.fbc.navigation.v1+json
```

Current version: v1 (default)

---

**API Contracts Completed**: September 8, 2025
**API Designer**: AI Assistant
**Review Status**: Approved for Implementation
