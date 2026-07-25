# Kraly Data Dictionary

## Table Overview

| Table | Purpose | Primary Key |
|---|---|---|
| `companies` | Stores customer organizations | `company_id` |
| `users` | Stores employees using Kraly | `user_id` |
| `plans` | Stores available subscription plans | `plan_id` |
| `subscriptions` | Stores customer subscription history | `subscription_id` |
| `projects` | Stores customer projects | `project_id` |
| `tasks` | Stores tasks within projects | `task_id` |
| `login_events` | Stores user login activity | `login_event_id` |
| `feature_usage_events` | Stores feature interactions | `feature_event_id` |
| `support_tickets` | Stores customer support requests | `ticket_id` |
| `invoices` | Stores customer invoices | `invoice_id` |
| `payments` | Stores invoice payment records | `payment_id` |

---

## 1. `companies`

**Purpose:** Stores information about customer organizations that subscribe to Kraly.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `company_id` | INTEGER | PK | Yes | Auto-generated | Unique company identifier |
| `company_name` | VARCHAR(150) | UNIQUE | Yes | Fictional business name | Company name |
| `industry` | VARCHAR(50) |  | Yes | Technology, healthcare, finance, retail, education, manufacturing, logistics | Company industry |
| `country` | VARCHAR(75) |  | Yes | Country name | Headquarters country |
| `company_size` | VARCHAR(20) |  | Yes | Small, medium, enterprise | Company size category |
| `created_at` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Date the company became a customer |
| `account_status` | VARCHAR(20) |  | Yes | Trial, active, suspended, churned | Current account status |

**Relationships**

- One company can have many users.
- One company can have many subscriptions.
- One company can have many projects.
- One company can have many support tickets.
- One company can have many invoices.

---

## 2. `users`

**Purpose:** Stores employees who use Kraly through a customer organization.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `user_id` | INTEGER | PK | Yes | Auto-generated | Unique user identifier |
| `company_id` | INTEGER | FK | Yes | References `companies.company_id` | Company the user belongs to |
| `first_name` | VARCHAR(50) |  | Yes | Text | First name |
| `last_name` | VARCHAR(50) |  | Yes | Text | Last name |
| `email` | VARCHAR(150) | UNIQUE | Yes | Valid work email | User email address |
| `department` | VARCHAR(50) |  | Yes | Engineering, product, data, HR, finance, marketing | User department |
| `job_role` | VARCHAR(75) |  | Yes | Text | User role |
| `signup_date` | DATE |  | Yes | `YYYY-MM-DD` | Date the account was created |
| `user_status` | VARCHAR(20) |  | Yes | Active, inactive, deactivated | Current user status |

**Relationships**

- Each user belongs to one company.
- One user can create many projects.
- One user can be assigned many tasks.
- One user can have many login events.
- One user can have many feature usage events.
- One user can submit many support tickets.

---

## 3. `plans`

**Purpose:** Stores Kraly’s available subscription plans and plan limits.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `plan_id` | INTEGER | PK | Yes | Auto-generated | Unique plan identifier |
| `plan_name` | VARCHAR(30) | UNIQUE | Yes | Starter, professional, enterprise | Subscription plan name |
| `monthly_price` | NUMERIC(10,2) |  | Yes | Amount in USD | Monthly base price |
| `max_users` | INTEGER |  | Yes | Positive whole number | Maximum users allowed |
| `storage_limit_gb` | INTEGER |  | Yes | Positive whole number | Included file storage in gigabytes |
| `api_access` | BOOLEAN |  | Yes | `TRUE` or `FALSE` | Whether API access is included |
| `ai_assistant_access` | BOOLEAN |  | Yes | `TRUE` or `FALSE` | Whether AI assistant access is included |
| `workflow_automation_access` | BOOLEAN |  | Yes | `TRUE` or `FALSE` | Whether workflow automation is included |
| `created_at` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Date the plan was created |
| `is_active` | BOOLEAN |  | Yes | `TRUE` or `FALSE` | Whether the plan is currently offered |

**Relationships**

- One plan can be used by many subscriptions.
- Each subscription references one plan.

---

## 4. `subscriptions`

**Purpose:** Stores each company’s subscription history, including upgrades, downgrades, renewals, and cancellations.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `subscription_id` | INTEGER | PK | Yes | Auto-generated | Unique subscription identifier |
| `company_id` | INTEGER | FK | Yes | References `companies.company_id` | Company purchasing the subscription |
| `plan_id` | INTEGER | FK | Yes | References `plans.plan_id` | Selected subscription plan |
| `start_date` | DATE |  | Yes | `YYYY-MM-DD` | Subscription start date |
| `end_date` | DATE |  | No | `YYYY-MM-DD` or null | Subscription end date |
| `billing_cycle` | VARCHAR(20) |  | Yes | Monthly, annual | Billing frequency |
| `subscription_status` | VARCHAR(20) |  | Yes | Trial, active, canceled, expired | Current subscription status |
| `seats_purchased` | INTEGER |  | Yes | Positive whole number | Number of user seats purchased |
| `monthly_recurring_revenue` | NUMERIC(12,2) |  | Yes | Amount in USD | Monthly recurring revenue associated with the subscription |
| `cancellation_reason` | VARCHAR(150) |  | No | Text or null | Reason the customer canceled |
| `created_at` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Date the subscription record was created |

**Relationships**

- Each subscription belongs to one company.
- Each subscription uses one plan.
- One company can have multiple subscription records over time.
- One subscription can generate many invoices.

---

## 5. `projects`

**Purpose:** Stores projects created by users within customer organizations.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `project_id` | INTEGER | PK | Yes | Auto-generated | Unique project identifier |
| `company_id` | INTEGER | FK | Yes | References `companies.company_id` | Company that owns the project |
| `created_by_user_id` | INTEGER | FK | Yes | References `users.user_id` | User who created the project |
| `project_name` | VARCHAR(150) |  | Yes | Text | Project name |
| `project_description` | TEXT |  | No | Text or null | Project summary |
| `created_at` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Project creation time |
| `due_date` | DATE |  | No | `YYYY-MM-DD` or null | Project due date |
| `completed_at` | TIMESTAMP |  | No | Timestamp or null | Project completion time |
| `project_status` | VARCHAR(20) |  | Yes | Planned, active, completed, archived | Current project status |
| `priority` | VARCHAR(20) |  | Yes | Low, medium, high, urgent | Project priority |

**Relationships**

- Each project belongs to one company.
- Each project is created by one user.
- One company can have many projects.
- One user can create many projects.
- One project can contain many tasks.

---

## 6. `tasks`

**Purpose:** Stores tasks created within projects.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `task_id` | INTEGER | PK | Yes | Auto-generated | Unique task identifier |
| `project_id` | INTEGER | FK | Yes | References `projects.project_id` | Project containing the task |
| `assigned_user_id` | INTEGER | FK | No | References `users.user_id` or null | User assigned to the task |
| `created_by_user_id` | INTEGER | FK | Yes | References `users.user_id` | User who created the task |
| `task_name` | VARCHAR(150) |  | Yes | Text | Task title |
| `task_description` | TEXT |  | No | Text or null | Task details |
| `priority` | VARCHAR(20) |  | Yes | Low, medium, high, urgent | Task priority |
| `created_at` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Task creation time |
| `due_date` | DATE |  | No | `YYYY-MM-DD` or null | Task due date |
| `completed_at` | TIMESTAMP |  | No | Timestamp or null | Task completion time |
| `task_status` | VARCHAR(20) |  | Yes | Open, in progress, completed, canceled | Current task status |

**Relationships**

- Each task belongs to one project.
- Each task is created by one user.
- A task may be assigned to one user.
- One project can contain many tasks.
- One user can create or be assigned many tasks.

---

## 7. `login_events`

**Purpose:** Stores user login activity and session information.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `login_event_id` | BIGINT | PK | Yes | Auto-generated | Unique login event identifier |
| `user_id` | INTEGER | FK | Yes | References `users.user_id` | User associated with the login |
| `login_timestamp` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Login date and time |
| `logout_timestamp` | TIMESTAMP |  | No | Timestamp or null | Logout date and time |
| `session_duration_minutes` | INTEGER |  | No | Zero or positive whole number | Length of the session |
| `device_type` | VARCHAR(20) |  | Yes | Desktop, mobile, tablet | Device used |
| `operating_system` | VARCHAR(30) |  | No | Windows, macOS, Linux, iOS, Android | Device operating system |
| `login_successful` | BOOLEAN |  | Yes | `TRUE` or `FALSE` | Whether the login attempt succeeded |
| `failure_reason` | VARCHAR(100) |  | No | Text or null | Reason a login attempt failed |

**Relationships**

- Each login event belongs to one user.
- One user can have many login events.

---

## 8. `feature_usage_events`

**Purpose:** Stores interactions with Kraly’s product features.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `feature_event_id` | BIGINT | PK | Yes | Auto-generated | Unique feature usage event identifier |
| `user_id` | INTEGER | FK | Yes | References `users.user_id` | User who performed the action |
| `company_id` | INTEGER | FK | Yes | References `companies.company_id` | User’s company |
| `feature_name` | VARCHAR(75) |  | Yes | Project management, task management, file sharing, reporting, workflow automation, API, AI assistant | Feature used |
| `event_name` | VARCHAR(75) |  | Yes | Created, viewed, edited, exported, uploaded, invited, generated | Type of action |
| `event_timestamp` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Date and time of the action |
| `session_id` | VARCHAR(100) |  | Yes | Unique session string | Session associated with the event |
| `project_id` | INTEGER | FK | No | References `projects.project_id` or null | Related project, when applicable |
| `usage_count` | INTEGER |  | Yes | Positive whole number | Number of recorded interactions |

**Relationships**

- Each feature event belongs to one user.
- Each feature event belongs to one company.
- A feature event may relate to one project.
- One user can generate many feature usage events.
- One company can generate many feature usage events.

---

## 9. `support_tickets`

**Purpose:** Stores customer support requests and resolution information.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `ticket_id` | INTEGER | PK | Yes | Auto-generated | Unique support ticket identifier |
| `company_id` | INTEGER | FK | Yes | References `companies.company_id` | Company that submitted the ticket |
| `submitted_by_user_id` | INTEGER | FK | Yes | References `users.user_id` | User who submitted the ticket |
| `category` | VARCHAR(50) |  | Yes | Billing, technical issue, account access, feature request, performance, other | Ticket category |
| `priority` | VARCHAR(20) |  | Yes | Low, medium, high, urgent | Ticket priority |
| `subject` | VARCHAR(150) |  | Yes | Text | Short ticket title |
| `description` | TEXT |  | Yes | Text | Full issue description |
| `created_at` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Ticket submission time |
| `first_response_at` | TIMESTAMP |  | No | Timestamp or null | Time of the first support response |
| `resolved_at` | TIMESTAMP |  | No | Timestamp or null | Ticket resolution time |
| `ticket_status` | VARCHAR(20) |  | Yes | Open, pending, resolved, closed | Current ticket status |
| `satisfaction_score` | INTEGER |  | No | 1 through 5 or null | Customer satisfaction rating |

**Relationships**

- Each support ticket belongs to one company.
- Each support ticket is submitted by one user.
- One company can have many support tickets.
- One user can submit many support tickets.

---

## 10. `invoices`

**Purpose:** Stores invoices issued for customer subscriptions.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `invoice_id` | INTEGER | PK | Yes | Auto-generated | Unique invoice identifier |
| `company_id` | INTEGER | FK | Yes | References `companies.company_id` | Customer company |
| `subscription_id` | INTEGER | FK | Yes | References `subscriptions.subscription_id` | Related subscription |
| `invoice_date` | DATE |  | Yes | `YYYY-MM-DD` | Date the invoice was issued |
| `billing_period_start` | DATE |  | Yes | `YYYY-MM-DD` | Start of the billing period |
| `billing_period_end` | DATE |  | Yes | `YYYY-MM-DD` | End of the billing period |
| `due_date` | DATE |  | Yes | `YYYY-MM-DD` | Payment due date |
| `subtotal` | NUMERIC(12,2) |  | Yes | Amount in USD | Amount before tax or credits |
| `tax_amount` | NUMERIC(12,2) |  | Yes | Amount in USD | Tax charged |
| `discount_amount` | NUMERIC(12,2) |  | Yes | Amount in USD | Discount applied |
| `amount_due` | NUMERIC(12,2) |  | Yes | Amount in USD | Final invoice amount |
| `invoice_status` | VARCHAR(20) |  | Yes | Pending, paid, overdue, canceled | Current invoice status |

**Relationships**

- Each invoice belongs to one company.
- Each invoice belongs to one subscription.
- One company can have many invoices.
- One subscription can produce many invoices.
- One invoice can have one or more payment attempts.

---

## 11. `payments`

**Purpose:** Stores payment attempts and completed payments for invoices.

| Column | Data Type | Key | Required | Allowed Values / Format | Description |
|---|---|---|---|---|---|
| `payment_id` | INTEGER | PK | Yes | Auto-generated | Unique payment identifier |
| `invoice_id` | INTEGER | FK | Yes | References `invoices.invoice_id` | Invoice being paid |
| `payment_date` | TIMESTAMP |  | Yes | `YYYY-MM-DD HH:MM:SS` | Date and time of payment attempt |
| `amount_paid` | NUMERIC(12,2) |  | Yes | Amount in USD | Amount paid |
| `payment_method` | VARCHAR(30) |  | Yes | Card, ACH, wire transfer | Payment method |
| `payment_status` | VARCHAR(20) |  | Yes | Successful, failed, pending, refunded | Current payment status |
| `transaction_reference` | VARCHAR(100) | UNIQUE | Yes | Generated transaction string | External payment reference |
| `failure_reason` | VARCHAR(100) |  | No | Text or null | Reason the payment failed |
| `refunded_at` | TIMESTAMP |  | No | Timestamp or null | Date and time the payment was refunded |

**Relationships**

- Each payment belongs to one invoice.
- One invoice can have multiple payment attempts.