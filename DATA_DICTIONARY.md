# Data Dictionary

This document provides a comprehensive reference for all database tables in the Churn Analytics system.

**Last Updated:** 2025-12-10  
**Database:** churn_analytics  
**Engine:** InnoDB  
**Character Set:** utf8mb4  
**Collation:** utf8mb4_unicode_ci

---

## Table of Contents

1. [users](#1-users)
2. [subscriptions](#2-subscriptions)
3. [Foreign Key Relationships](#foreign-key-relationships)

---

## 1. users

**Table Type:** Dimension Table  
**Description:** User demographic information and profile attributes. Contains original users from Kaggle dataset plus approximately 20% fake users (registered but without subscriptions) to simulate real-world scenarios.

### Table Structure

| Field Name | Data Type | Nullable | Default | Key Type | Description |
|------------|-----------|----------|---------|----------|-------------|
| user_id | VARCHAR(50) | NOT NULL | - | PRIMARY KEY | Unique user identifier (format: XXXX-XXXXX) |
| gender | VARCHAR(10) | NULL | NULL | - | User gender (Male/Female) |
| senior_citizen | TINYINT(1) | NULL | NULL | - | Whether user is a senior citizen (0=No, 1=Yes) |
| has_partner | TINYINT(1) | NULL | NULL | - | Whether user has a partner (0=No, 1=Yes) |
| has_dependents | TINYINT(1) | NULL | NULL | - | Whether user has dependents (0=No, 1=Yes) |

### Indexes

- **PRIMARY KEY:** `user_id`
- **INDEX:** `idx_user_id` on `user_id`

### Notes

- This is a dimension table in the star schema design
- Total records: 8,451 users
  - Original users: 7,043 (from Kaggle Telco Churn dataset)
  - Fake users: 1,408 (~17%, registered but no subscription)
- Approximately 17% of users are "fake users" (registered but no subscription)
- All user IDs follow the format: 4 digits, hyphen, 5 uppercase letters (e.g., "1234-ABCDE")
- Used as the primary dimension for user-level analysis

---

## 2. subscriptions

**Table Type:** Fact Table  
**Description:** Subscription lifecycle and service subscription information. Contains one record per user with subscription details, payment information, and service subscriptions. Only generated for original users (not fake users).

### Table Structure

| Field Name | Data Type | Nullable | Default | Key Type | Description |
|------------|-----------|----------|---------|----------|-------------|
| user_id | VARCHAR(50) | NOT NULL | - | PRIMARY KEY, FOREIGN KEY | User identifier (references users.user_id) |
| signup_date | DATE | NOT NULL | - | - | Date when user signed up for subscription |
| cancel_date | DATE | NULL | NULL | - | Date when user cancelled subscription (NULL for active users) |
| plan | VARCHAR(50) | NULL | NULL | - | Subscription plan type (Basic/Standard/Premium) |
| price | DECIMAL(10,2) | NULL | NULL | - | Monthly subscription price |
| status | ENUM('active', 'cancelled') | NULL | NULL | - | Subscription status |
| payment_method | VARCHAR(50) | NULL | NULL | - | Payment method used |
| total_charges | DECIMAL(10,2) | NULL | NULL | - | Total historical charges (may have deviations for discounts/promotions) |
| internet_service | VARCHAR(20) | NULL | NULL | - | Internet service type (DSL/Fiber optic/No) |
| phone_service | TINYINT(1) | NULL | 0 | - | Whether user has phone service (0=No, 1=Yes) |
| multiple_lines | TINYINT(1) | NULL | 0 | - | Whether user has multiple phone lines (0=No, 1=Yes) |
| online_security | TINYINT(1) | NULL | 0 | - | Whether user has online security service (0=No, 1=Yes) |
| online_backup | TINYINT(1) | NULL | 0 | - | Whether user has online backup service (0=No, 1=Yes) |
| device_protection | TINYINT(1) | NULL | 0 | - | Whether user has device protection service (0=No, 1=Yes) |
| tech_support | TINYINT(1) | NULL | 0 | - | Whether user has tech support service (0=No, 1=Yes) |
| streaming_tv | TINYINT(1) | NULL | 0 | - | Whether user has streaming TV service (0=No, 1=Yes) |
| streaming_movies | TINYINT(1) | NULL | 0 | - | Whether user has streaming movies service (0=No, 1=Yes) |
| paperless_billing | TINYINT(1) | NULL | 0 | - | Whether user has paperless billing enabled (0=No, 1=Yes) |

### Indexes

- **PRIMARY KEY:** `user_id`
- **INDEX:** `idx_signup_date` on `signup_date`
- **INDEX:** `idx_status` on `status`
- **INDEX:** `idx_plan` on `plan`
- **INDEX:** `idx_user_id` on `user_id`

### Foreign Keys

- **FOREIGN KEY:** `user_id` → `users.user_id`
  - **ON DELETE:** CASCADE
  - **ON UPDATE:** CASCADE

### Business Rules

1. **Service Dependencies:**
   - If `internet_service` = 'No', then all online services (`online_security`, `online_backup`, `device_protection`, `streaming_tv`, `streaming_movies`) must be 0
   - If `phone_service` = 0, then `multiple_lines` must be 0

2. **Plan Inference:**
   - Plan type is inferred based on Contract, MonthlyCharges, and InternetService
   - Basic: Lower tier plans
   - Standard: Mid-tier plans
   - Premium: Higher tier plans

---

## Foreign Key Relationships

### Relationship Diagram

```
users (Dimension Table)
  │
  │ 1:1 (for subscribed users)
  │ 1:0 (for fake users)
  │
  └──> subscriptions (Fact Table)
        └── user_id (FK) → users.user_id (PK)
```

### Detailed Relationships

| Child Table | Child Column | Parent Table | Parent Column | Relationship Type | Delete Rule | Update Rule |
|-------------|--------------|--------------|---------------|-------------------|-------------|--------------|
| subscriptions | user_id | users | user_id | One-to-One (for subscribed users) | CASCADE | CASCADE |

### Relationship Notes

1. **users → subscriptions:**
   - **Cardinality:** One-to-One (for users with subscriptions), One-to-Zero (for fake users)
   - **Optionality:** subscriptions.user_id is NOT NULL, but not all users have subscriptions
   - **Cascade Behavior:** 
     - If a user is deleted, their subscription is automatically deleted
     - If a user_id is updated, the subscription.user_id is automatically updated
   - **Business Logic:** 
     - Approximately 80% of users have subscriptions (original users)
     - Approximately 20% of users are "fake users" with no subscriptions
     - This simulates real-world scenarios where users register but never subscribe

### Data Integrity

- All `subscriptions.user_id` values must exist in `users.user_id`
- No orphaned subscription records can exist
- Foreign key constraint ensures referential integrity

---

## Additional Notes

### user_events Table (CSV Only)

The `user_events` table is **not** stored in MySQL. It is maintained as a CSV file (`data/user_events.csv`) to simulate message queue or stream data processing scenarios.

**Structure (CSV):**
- `user_id` (VARCHAR): User identifier
- `event_type` (VARCHAR): Event type (login/watch/click/cancel)
- `event_time` (DATETIME): Event timestamp (constrained to 2023-01-01 through 2025-12-31)
- `device_type` (VARCHAR): Device type (mobile/desktop/tablet)
- `page_url` (VARCHAR): Page URL where event occurred

**Data Volume:**
- Approximately 21.7 million event records
- File size: ~1.1GB
- Events are generated only for users with subscriptions (7,043 users)
- Event timestamps are validated to ensure they fall within the user's subscription lifecycle and the 2023-2025 time range

**Why CSV:**
- Simulates real-world streaming data scenarios
- Better suited for analysis in Notebook/Spark environments
- Avoids database storage overhead for high-volume event data
- Supports time-series and behavioral analysis workflows

---

## Contact

For questions or updates to this data dictionary, please refer to the project README.md or contact the data engineering team.

