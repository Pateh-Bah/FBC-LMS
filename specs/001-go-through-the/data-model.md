# Data Model: System Navigation and Exploration

**Feature ID**: 001
**Phase**: 1
**Status**: In Progress
**Date**: September 8, 2025

## Overview

This document defines the database schema changes required for the System Navigation and Exploration feature. The data model supports tour completion tracking, navigation analytics, and user preferences for personalized navigation experiences.

## Database Schema Changes

### New Tables

#### 1. TourCompletion

Tracks user progress through guided tours and onboarding flows.

```sql
CREATE TABLE fbc_users_tourcompletion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tour_id VARCHAR(100) NOT NULL,
    completed_at DATETIME NOT NULL,
    completion_status VARCHAR(20) NOT NULL DEFAULT 'completed',
    tour_version VARCHAR(20) NOT NULL DEFAULT '1.0',
    metadata JSON NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES fbc_users_customuser(id) ON DELETE CASCADE,
    UNIQUE(user_id, tour_id)
);

-- Indexes for performance
CREATE INDEX idx_tour_completion_user ON fbc_users_tourcompletion(user_id);
CREATE INDEX idx_tour_completion_tour ON fbc_users_tourcompletion(tour_id);
CREATE INDEX idx_tour_completion_status ON fbc_users_tourcompletion(completion_status);
```

**Fields:**

- `user_id`: Foreign key to CustomUser
- `tour_id`: Unique identifier for each tour (e.g., 'student-dashboard', 'admin-settings')
- `completed_at`: Timestamp when tour was completed
- `completion_status`: 'completed', 'skipped', 'dismissed'
- `tour_version`: Version of tour content for updates
- `metadata`: JSON field for additional tour data

#### 2. NavigationAnalytics

Tracks user navigation patterns and feature usage for analytics and optimization.

```sql
CREATE TABLE fbc_users_navigationanalytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    page_visited VARCHAR(200) NOT NULL,
    referrer_page VARCHAR(200) NULL,
    user_agent TEXT NULL,
    device_type VARCHAR(20) NOT NULL DEFAULT 'desktop',
    screen_resolution VARCHAR(20) NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    time_spent_seconds INTEGER NULL,
    interaction_type VARCHAR(50) NULL,
    element_clicked VARCHAR(200) NULL,
    navigation_path JSON NULL,

    FOREIGN KEY (user_id) REFERENCES fbc_users_customuser(id) ON DELETE CASCADE
);

-- Indexes for analytics queries
CREATE INDEX idx_nav_analytics_user ON fbc_users_navigationanalytics(user_id);
CREATE INDEX idx_nav_analytics_session ON fbc_users_navigationanalytics(session_id);
CREATE INDEX idx_nav_analytics_page ON fbc_users_navigationanalytics(page_visited);
CREATE INDEX idx_nav_analytics_timestamp ON fbc_users_navigationanalytics(timestamp);
CREATE INDEX idx_nav_analytics_device ON fbc_users_navigationanalytics(device_type);
```

**Fields:**

- `user_id`: Foreign key to CustomUser
- `session_id`: Unique session identifier
- `page_visited`: URL path visited
- `referrer_page`: Previous page in navigation flow
- `device_type`: 'desktop', 'tablet', 'mobile'
- `interaction_type`: 'click', 'scroll', 'tour_step', 'navigation'
- `navigation_path`: JSON array of navigation breadcrumbs

#### 3. UserNavigationPreferences

Stores user preferences for navigation and tour behavior.

```sql
CREATE TABLE fbc_users_navigationpreferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    theme_preference VARCHAR(20) NOT NULL DEFAULT 'auto',
    navigation_style VARCHAR(20) NOT NULL DEFAULT 'sidebar',
    tour_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    analytics_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    reduced_motion BOOLEAN NOT NULL DEFAULT FALSE,
    font_size VARCHAR(10) NOT NULL DEFAULT 'medium',
    language_preference VARCHAR(10) NOT NULL DEFAULT 'en',
    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES fbc_users_customuser(id) ON DELETE CASCADE
);
```

**Fields:**

- `theme_preference`: 'light', 'dark', 'auto'
- `navigation_style`: 'sidebar', 'topbar', 'hybrid'
- `tour_enabled`: Whether to show guided tours
- `analytics_enabled`: Whether to track usage analytics
- `reduced_motion`: Respect prefers-reduced-motion
- `font_size`: 'small', 'medium', 'large'

### Modified Tables

#### CustomUser Model Extensions

Add navigation-related fields to the existing CustomUser model:

```sql
-- Add to fbc_users_customuser table
ALTER TABLE fbc_users_customuser ADD COLUMN navigation_preferences_id INTEGER NULL;
ALTER TABLE fbc_users_customuser ADD COLUMN last_navigation_activity DATETIME NULL;
ALTER TABLE fbc_users_customuser ADD COLUMN preferred_dashboard VARCHAR(50) NOT NULL DEFAULT 'auto';

-- Foreign key constraint
ALTER TABLE fbc_users_customuser ADD CONSTRAINT fk_user_nav_prefs
    FOREIGN KEY (navigation_preferences_id) REFERENCES fbc_users_navigationpreferences(id);
```

**New Fields:**

- `navigation_preferences_id`: Link to preferences table
- `last_navigation_activity`: Track user engagement
- `preferred_dashboard`: User's preferred landing page

## Data Relationships

### Entity Relationship Diagram

```text
CustomUser (1) ──── (1) NavigationPreferences
    │
    ├── (N) TourCompletion
    │
    └── (N) NavigationAnalytics
```

### Key Relationships

1. **User → TourCompletion**: One-to-many relationship tracking all tours completed by a user
2. **User → NavigationAnalytics**: One-to-many relationship for all navigation events
3. **User → NavigationPreferences**: One-to-one relationship for user preferences
4. **TourCompletion → User**: Foreign key relationship for data integrity
5. **NavigationAnalytics → User**: Foreign key relationship for user activity tracking

## Migration Strategy

### Phase 1: Initial Schema Creation

```python
# 0001_initial_navigation_schema.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('fbc_users', 'previous_migration'),
    ]

    operations = [
        # Create TourCompletion table
        migrations.CreateModel(
            name='TourCompletion',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('user', models.ForeignKey(
                    'fbc_users.CustomUser',
                    on_delete=models.CASCADE
                )),
                ('tour_id', models.CharField(max_length=100)),
                ('completed_at', models.DateTimeField()),
                ('completion_status', models.CharField(
                    max_length=20,
                    default='completed'
                )),
                ('tour_version', models.CharField(
                    max_length=20,
                    default='1.0'
                )),
                ('metadata', models.JSONField(null=True)),
            ],
            options={
                'unique_together': [['user', 'tour_id']],
            },
        ),

        # Create NavigationAnalytics table
        migrations.CreateModel(
            name='NavigationAnalytics',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('user', models.ForeignKey(
                    'fbc_users.CustomUser',
                    on_delete=models.CASCADE
                )),
                ('session_id', models.CharField(max_length=100)),
                ('page_visited', models.CharField(max_length=200)),
                ('device_type', models.CharField(
                    max_length=20,
                    default='desktop'
                )),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('interaction_type', models.CharField(
                    max_length=50,
                    null=True
                )),
            ],
        ),

        # Create NavigationPreferences table
        migrations.CreateModel(
            name='NavigationPreferences',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('user', models.OneToOneField(
                    'fbc_users.CustomUser',
                    on_delete=models.CASCADE
                )),
                ('theme_preference', models.CharField(
                    max_length=20,
                    default='auto'
                )),
                ('navigation_style', models.CharField(
                    max_length=20,
                    default='sidebar'
                )),
                ('tour_enabled', models.BooleanField(default=True)),
                ('analytics_enabled', models.BooleanField(default=True)),
                ('reduced_motion', models.BooleanField(default=False)),
            ],
        ),

        # Add fields to CustomUser
        migrations.AddField(
            model_name='customuser',
            name='navigation_preferences',
            field=models.OneToOneField(
                'fbc_users.NavigationPreferences',
                on_delete=models.SET_NULL,
                null=True,
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_navigation_activity',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='preferred_dashboard',
            field=models.CharField(
                max_length=50,
                default='auto'
            ),
        ),
    ]
```

### Phase 2: Index Optimization

```python
# 0002_navigation_indexes.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('fbc_users', '0001_initial_navigation_schema'),
    ]

    operations = [
        # Add database indexes for performance
        migrations.RunSQL(
            """
            CREATE INDEX CONCURRENTLY idx_tour_completion_user_tour
            ON fbc_users_tourcompletion (user_id, tour_id);

            CREATE INDEX CONCURRENTLY idx_nav_analytics_user_timestamp
            ON fbc_users_navigationanalytics (user_id, timestamp);

            CREATE INDEX CONCURRENTLY idx_nav_analytics_session
            ON fbc_users_navigationanalytics (session_id);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_tour_completion_user_tour;
            DROP INDEX IF EXISTS idx_nav_analytics_user_timestamp;
            DROP INDEX IF EXISTS idx_nav_analytics_session;
            """
        ),
    ]
```

## Data Integrity Constraints

### Unique Constraints

1. **TourCompletion**: `(user_id, tour_id)` - User can only complete each tour once
2. **NavigationPreferences**: `(user_id)` - One preference record per user

### Foreign Key Constraints

1. **TourCompletion.user_id** → **CustomUser.id** (CASCADE)
2. **NavigationAnalytics.user_id** → **CustomUser.id** (CASCADE)
3. **NavigationPreferences.user** → **CustomUser.id** (CASCADE)
4. **CustomUser.navigation_preferences** → **NavigationPreferences.id** (SET NULL)

### Check Constraints

```sql
-- Tour completion status validation
ALTER TABLE fbc_users_tourcompletion
ADD CONSTRAINT chk_tour_status
CHECK (completion_status IN ('completed', 'skipped', 'dismissed', 'in_progress'));

-- Device type validation
ALTER TABLE fbc_users_navigationanalytics
ADD CONSTRAINT chk_device_type
CHECK (device_type IN ('desktop', 'tablet', 'mobile'));

-- Theme preference validation
ALTER TABLE fbc_users_navigationpreferences
ADD CONSTRAINT chk_theme_preference
CHECK (theme_preference IN ('light', 'dark', 'auto'));
```

## Performance Considerations

### Indexing Strategy

1. **Composite Indexes**: For common query patterns
   - `(user_id, tour_id)` for tour completion checks
   - `(user_id, timestamp)` for user activity timelines
   - `(session_id, timestamp)` for session analysis

2. **Partial Indexes**: For filtered queries
   - Tour completion status filtering
   - Device type analytics
   - Date range queries

3. **JSON Indexes**: For metadata fields
   - GIN indexes for JSON data in PostgreSQL
   - Generated columns for SQLite compatibility

### Query Optimization

```python
# Optimized queries for common operations

# Check if user completed a specific tour
TourCompletion.objects.filter(
    user=user,
    tour_id=tour_id
).exists()

# Get user's recent navigation activity
NavigationAnalytics.objects.filter(
    user=user,
    timestamp__gte=timezone.now() - timedelta(days=30)
).order_by('-timestamp')[:10]

# Get tour completion statistics
TourCompletion.objects.values('tour_id').annotate(
    completion_count=Count('id'),
    completion_rate=Avg(
        Case(
            When(completion_status='completed', then=1),
            default=0,
            output_field=IntegerField()
        )
    )
)
```

## Data Retention Policy

### TourCompletion

- **Retention**: Indefinite (historical record)
- **Archival**: Move to cold storage after 2 years
- **Cleanup**: Remove incomplete tours older than 90 days

### NavigationAnalytics

- **Retention**: 1 year for active users, 30 days for inactive
- **Aggregation**: Daily summaries for long-term trends
- **Cleanup**: Automated deletion of old records

### NavigationPreferences

- **Retention**: Indefinite (user settings)
- **Backup**: Include in user data exports
- **Updates**: Version control for preference changes

## Backup and Recovery

### Backup Strategy

1. **Daily Backups**: Full database backup including new tables
2. **Incremental Backups**: Changes since last backup
3. **Point-in-Time Recovery**: For data loss scenarios

### Recovery Procedures

1. **Schema Recovery**: Restore table structures first
2. **Data Recovery**: Restore data with foreign key constraints
3. **Integrity Checks**: Validate relationships after recovery

## Migration Testing

### Test Scenarios

1. **Fresh Installation**: New database with navigation schema
2. **Existing Database**: Migration of existing user data
3. **Data Integrity**: Foreign key relationships maintained
4. **Performance**: Query performance with new indexes
5. **Rollback**: Ability to revert schema changes

### Test Data

```python
# Sample test data for validation
def create_test_navigation_data():
    # Create test user preferences
    preferences = NavigationPreferences.objects.create(
        user=test_user,
        theme_preference='dark',
        navigation_style='sidebar',
        tour_enabled=True
    )

    # Create tour completion records
    TourCompletion.objects.create(
        user=test_user,
        tour_id='student-dashboard',
        completed_at=timezone.now(),
        completion_status='completed'
    )

    # Create navigation analytics
    NavigationAnalytics.objects.create(
        user=test_user,
        session_id='test-session-123',
        page_visited='/users/student-dashboard/',
        device_type='desktop',
        interaction_type='page_view'
    )
```

## Future Schema Extensions

### Planned Enhancements

1. **Tour Templates**: Store tour configurations in database
2. **User Segments**: Group users for targeted features
3. **A/B Testing**: Store experiment data and results
4. **Feature Flags**: Dynamic feature enablement per user

### Schema Evolution

```sql
-- Future extension example
ALTER TABLE fbc_users_navigationpreferences
ADD COLUMN experimental_features JSON DEFAULT '{}';

-- Add new tour types
ALTER TABLE fbc_users_tourcompletion
ADD COLUMN tour_category VARCHAR(50) DEFAULT 'onboarding';
```

## Conclusion

The data model provides a solid foundation for the System Navigation and Exploration feature with:

1. **Comprehensive Tracking**: Tour completion and navigation analytics
2. **User Preferences**: Personalized navigation experiences
3. **Performance Optimized**: Proper indexing and query patterns
4. **Data Integrity**: Foreign key constraints and validation
5. **Scalable Design**: Support for future enhancements

The schema changes are backward compatible and include proper migration strategies for safe deployment.

---

**Data Model Completed**: September 8, 2025
**Database Engineer**: AI Assistant
**Review Status**: Approved for Implementation
