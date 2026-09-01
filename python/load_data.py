from pathlib import Path
import os

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "generated"

DB_NAME = "enterprise_saas_analytics"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5433"

DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

if not DB_PASSWORD:
    raise ValueError(
        "POSTGRES_PASSWORD environment variable is not set."
    )


# ---------------------------------------------------------
# CONNECT TO POSTGRESQL
# ---------------------------------------------------------

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)

cursor = conn.cursor()

print("\nConnected to PostgreSQL successfully.")


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def load_csv(table_name, csv_file, columns):
    print(f"Loading {table_name}...")

    df = pd.read_csv(DATA_DIR / csv_file)

    # Convert pandas NaN values into Python None
    # astype(object) is needed so nullable numeric columns can actually hold None
    df = df.astype(object).where(pd.notnull(df), None)

    rows = [
        tuple(row)
        for row in df[columns].itertuples(index=False, name=None)
    ]

    column_names = ", ".join(columns)

    query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES %s
    """

    execute_values(
        cursor,
        query,
        rows,
        page_size=5000,
    )

    conn.commit()

    print(f"Loaded {len(df):,} rows into {table_name}.")


# ---------------------------------------------------------
# LOAD TABLES IN FOREIGN KEY ORDER
# ---------------------------------------------------------

load_csv(
    "plans",
    "plans.csv",
    [
        "plan_id",
        "plan_name",
        "monthly_price",
        "max_users",
        "storage_limit_gb",
        "api_access",
        "ai_assistant_access",
        "workflow_automation_access",
        "created_at",
        "is_active",
    ],
)

load_csv(
    "companies",
    "companies.csv",
    [
        "company_id",
        "company_name",
        "industry",
        "country",
        "company_size",
        "created_at",
        "account_status",
    ],
)

load_csv(
    "users",
    "users.csv",
    [
        "user_id",
        "company_id",
        "first_name",
        "last_name",
        "email",
        "department",
        "job_role",
        "signup_date",
        "user_status",
    ],
)

load_csv(
    "subscriptions",
    "subscriptions.csv",
    [
        "subscription_id",
        "company_id",
        "plan_id",
        "start_date",
        "end_date",
        "billing_cycle",
        "subscription_status",
        "seats_purchased",
        "monthly_recurring_revenue",
        "cancellation_reason",
        "created_at",
    ],
)

load_csv(
    "projects",
    "projects.csv",
    [
        "project_id",
        "company_id",
        "created_by_user_id",
        "project_name",
        "project_description",
        "created_at",
        "due_date",
        "completed_at",
        "project_status",
        "priority",
    ],
)

load_csv(
    "tasks",
    "tasks.csv",
    [
        "task_id",
        "project_id",
        "assigned_user_id",
        "created_by_user_id",
        "task_name",
        "task_description",
        "priority",
        "created_at",
        "due_date",
        "completed_at",
        "task_status",
    ],
)

load_csv(
    "login_events",
    "login_events.csv",
    [
        "login_event_id",
        "user_id",
        "login_timestamp",
        "logout_timestamp",
        "session_duration_minutes",
        "device_type",
        "operating_system",
        "login_successful",
        "failure_reason",
    ],
)

load_csv(
    "feature_usage_events",
    "feature_usage_events.csv",
    [
        "feature_event_id",
        "user_id",
        "company_id",
        "project_id",
        "feature_name",
        "event_name",
        "event_timestamp",
        "session_id",
        "usage_count",
    ],
)

load_csv(
    "support_tickets",
    "support_tickets.csv",
    [
        "ticket_id",
        "company_id",
        "submitted_by_user_id",
        "category",
        "priority",
        "subject",
        "description",
        "created_at",
        "first_response_at",
        "resolved_at",
        "ticket_status",
        "satisfaction_score",
    ],
)

load_csv(
    "invoices",
    "invoices.csv",
    [
        "invoice_id",
        "company_id",
        "subscription_id",
        "invoice_date",
        "billing_period_start",
        "billing_period_end",
        "due_date",
        "subtotal",
        "tax_amount",
        "discount_amount",
        "amount_due",
        "invoice_status",
    ],
)

load_csv(
    "payments",
    "payments.csv",
    [
        "payment_id",
        "invoice_id",
        "payment_date",
        "amount_paid",
        "payment_method",
        "payment_status",
        "transaction_reference",
        "failure_reason",
        "refunded_at",
    ],
)


# ---------------------------------------------------------
# CLEANUP
# ---------------------------------------------------------

cursor.close()
conn.close()

print("\nAll data loaded successfully.")