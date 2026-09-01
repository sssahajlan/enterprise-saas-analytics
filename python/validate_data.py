from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "generated"

print("\nRunning data validation checks...")
print("---------------------------------")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

plans = pd.read_csv(DATA_DIR / "plans.csv")
companies = pd.read_csv(DATA_DIR / "companies.csv")
users = pd.read_csv(DATA_DIR / "users.csv")
subscriptions = pd.read_csv(DATA_DIR / "subscriptions.csv")
projects = pd.read_csv(DATA_DIR / "projects.csv")
tasks = pd.read_csv(DATA_DIR / "tasks.csv")
login_events = pd.read_csv(DATA_DIR / "login_events.csv")
feature_usage = pd.read_csv(DATA_DIR / "feature_usage_events.csv")
support_tickets = pd.read_csv(DATA_DIR / "support_tickets.csv")
invoices = pd.read_csv(DATA_DIR / "invoices.csv")
payments = pd.read_csv(DATA_DIR / "payments.csv")


# ---------------------------------------------------------
# VALIDATION HELPERS
# ---------------------------------------------------------

errors = []


def pass_check(message):
    print(f"PASS: {message}")


def fail_check(message):
    print(f"FAIL: {message}")
    errors.append(message)


def check_unique_primary_key(df, column, table_name):
    if df[column].is_unique and df[column].notna().all():
        pass_check(f"{table_name}.{column} is unique and not null")
    else:
        fail_check(f"{table_name}.{column} contains duplicates or nulls")


def check_foreign_key(
    child_df,
    child_column,
    parent_df,
    parent_column,
    relationship_name,
    allow_null=False,
):
    child_values = child_df[child_column]

    if allow_null:
        child_values = child_values.dropna()

    invalid_values = ~child_values.isin(parent_df[parent_column])

    if invalid_values.any():
        fail_check(
            f"{relationship_name} contains invalid foreign key values"
        )
    else:
        pass_check(f"{relationship_name} foreign keys are valid")


# ---------------------------------------------------------
# 1. PRIMARY KEY CHECKS
# ---------------------------------------------------------

print("\n1. Primary Keys")

check_unique_primary_key(plans, "plan_id", "plans")
check_unique_primary_key(companies, "company_id", "companies")
check_unique_primary_key(users, "user_id", "users")
check_unique_primary_key(
    subscriptions,
    "subscription_id",
    "subscriptions"
)
check_unique_primary_key(projects, "project_id", "projects")
check_unique_primary_key(tasks, "task_id", "tasks")
check_unique_primary_key(
    login_events,
    "login_event_id",
    "login_events"
)
check_unique_primary_key(
    feature_usage,
    "feature_event_id",
    "feature_usage_events"
)
check_unique_primary_key(
    support_tickets,
    "ticket_id",
    "support_tickets"
)
check_unique_primary_key(invoices, "invoice_id", "invoices")
check_unique_primary_key(payments, "payment_id", "payments")


# ---------------------------------------------------------
# 2. FOREIGN KEY CHECKS
# ---------------------------------------------------------

print("\n2. Foreign Keys")

check_foreign_key(
    users,
    "company_id",
    companies,
    "company_id",
    "users -> companies",
)

check_foreign_key(
    subscriptions,
    "company_id",
    companies,
    "company_id",
    "subscriptions -> companies",
)

check_foreign_key(
    subscriptions,
    "plan_id",
    plans,
    "plan_id",
    "subscriptions -> plans",
)

check_foreign_key(
    projects,
    "company_id",
    companies,
    "company_id",
    "projects -> companies",
)

check_foreign_key(
    projects,
    "created_by_user_id",
    users,
    "user_id",
    "projects -> users",
)

check_foreign_key(
    tasks,
    "project_id",
    projects,
    "project_id",
    "tasks -> projects",
)

check_foreign_key(
    tasks,
    "assigned_user_id",
    users,
    "user_id",
    "tasks assigned user -> users",
    allow_null=True,
)

check_foreign_key(
    tasks,
    "created_by_user_id",
    users,
    "user_id",
    "tasks creator -> users",
)

check_foreign_key(
    login_events,
    "user_id",
    users,
    "user_id",
    "login_events -> users",
)

check_foreign_key(
    feature_usage,
    "user_id",
    users,
    "user_id",
    "feature_usage -> users",
)

check_foreign_key(
    feature_usage,
    "company_id",
    companies,
    "company_id",
    "feature_usage -> companies",
)

check_foreign_key(
    feature_usage,
    "project_id",
    projects,
    "project_id",
    "feature_usage -> projects",
    allow_null=True,
)

check_foreign_key(
    support_tickets,
    "company_id",
    companies,
    "company_id",
    "support_tickets -> companies",
)

check_foreign_key(
    support_tickets,
    "submitted_by_user_id",
    users,
    "user_id",
    "support_tickets -> users",
)

check_foreign_key(
    invoices,
    "company_id",
    companies,
    "company_id",
    "invoices -> companies",
)

check_foreign_key(
    invoices,
    "subscription_id",
    subscriptions,
    "subscription_id",
    "invoices -> subscriptions",
)

check_foreign_key(
    payments,
    "invoice_id",
    invoices,
    "invoice_id",
    "payments -> invoices",
)


# ---------------------------------------------------------
# 3. REQUIRED FIELD CHECKS
# ---------------------------------------------------------

print("\n3. Required Fields")

required_columns = {
    "companies": (
        companies,
        [
            "company_id",
            "company_name",
            "industry",
            "country",
            "company_size",
            "created_at",
            "account_status",
        ],
    ),
    "users": (
        users,
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
    ),
    "subscriptions": (
        subscriptions,
        [
            "subscription_id",
            "company_id",
            "plan_id",
            "start_date",
            "billing_cycle",
            "subscription_status",
            "seats_purchased",
            "monthly_recurring_revenue",
        ],
    ),
}

for table_name, (df, columns) in required_columns.items():

    for column in columns:

        if df[column].notna().all():
            pass_check(f"{table_name}.{column} has no missing values")
        else:
            fail_check(f"{table_name}.{column} contains missing values")


# ---------------------------------------------------------
# 4. BUSINESS RULE CHECKS
# ---------------------------------------------------------

print("\n4. Business Rules")

# Subscription seats must not exceed plan limits
subscription_plan_check = subscriptions.merge(
    plans[["plan_id", "max_users"]],
    on="plan_id",
    how="left",
)

invalid_seats = (
    subscription_plan_check["seats_purchased"]
    > subscription_plan_check["max_users"]
)

if invalid_seats.any():
    fail_check("Some subscriptions exceed their plan's max_users")
else:
    pass_check("All subscription seat counts fit their plans")


# Churned companies should have canceled subscriptions
churned_company_ids = companies.loc[
    companies["account_status"] == "churned",
    "company_id",
]

invalid_churn = subscriptions[
    subscriptions["company_id"].isin(churned_company_ids)
    & (subscriptions["subscription_status"] != "canceled")
]

if len(invalid_churn) > 0:
    fail_check(
        "Some churned companies do not have canceled subscriptions"
    )
else:
    pass_check(
        "Churned companies have canceled subscriptions"
    )


# Completed tasks should have completed_at
completed_tasks = tasks[
    tasks["task_status"] == "completed"
]

if completed_tasks["completed_at"].notna().all():
    pass_check("Completed tasks have completion timestamps")
else:
    fail_check("Some completed tasks are missing completed_at")


# Non-completed tasks should generally not have completed_at
non_completed_tasks = tasks[
    tasks["task_status"] != "completed"
]

if non_completed_tasks["completed_at"].isna().all():
    pass_check("Non-completed tasks do not have completion timestamps")
else:
    fail_check(
        "Some non-completed tasks contain completed_at values"
    )


# Failed logins should have failure reasons
failed_logins = login_events[
    login_events["login_successful"] == False
]

if failed_logins["failure_reason"].notna().all():
    pass_check("Failed logins contain failure reasons")
else:
    fail_check("Some failed logins are missing failure reasons")


# Successful logins should have session durations
successful_logins = login_events[
    login_events["login_successful"] == True
]

if successful_logins[
    "session_duration_minutes"
].notna().all():
    pass_check("Successful logins contain session durations")
else:
    fail_check(
        "Some successful logins are missing session durations"
    )


# Successful payments should have positive payment amounts
successful_payments = payments[
    payments["payment_status"] == "successful"
]

if (
    successful_payments["amount_paid"] > 0
).all():
    pass_check("Successful payments have positive amounts")
else:
    fail_check(
        "Some successful payments do not have positive amounts"
    )


# Failed payments should have failure reasons
failed_payments = payments[
    payments["payment_status"] == "failed"
]

if failed_payments["failure_reason"].notna().all():
    pass_check("Failed payments contain failure reasons")
else:
    fail_check("Some failed payments are missing failure reasons")


# Satisfaction scores must be between 1 and 5
scores = support_tickets[
    "satisfaction_score"
].dropna()

if scores.between(1, 5).all():
    pass_check("Support satisfaction scores are between 1 and 5")
else:
    fail_check("Invalid support satisfaction scores found")


# ---------------------------------------------------------
# 5. DATE CHECKS
# ---------------------------------------------------------

print("\n5. Date Checks")

subscriptions["start_date"] = pd.to_datetime(
    subscriptions["start_date"]
)

subscriptions["end_date"] = pd.to_datetime(
    subscriptions["end_date"],
    errors="coerce",
)

invalid_subscription_dates = subscriptions[
    subscriptions["end_date"].notna()
    & (
        subscriptions["end_date"]
        < subscriptions["start_date"]
    )
]

if len(invalid_subscription_dates) == 0:
    pass_check("Subscription dates are valid")
else:
    fail_check("Some subscriptions end before they start")


tasks["created_at"] = pd.to_datetime(
    tasks["created_at"]
)

tasks["completed_at"] = pd.to_datetime(
    tasks["completed_at"],
    errors="coerce",
)

invalid_task_dates = tasks[
    tasks["completed_at"].notna()
    & (
        tasks["completed_at"]
        < tasks["created_at"]
    )
]

if len(invalid_task_dates) == 0:
    pass_check("Task completion dates occur after creation")
else:
    fail_check(
        "Some tasks were completed before they were created"
    )


support_tickets["created_at"] = pd.to_datetime(
    support_tickets["created_at"]
)

support_tickets["resolved_at"] = pd.to_datetime(
    support_tickets["resolved_at"],
    errors="coerce",
)

invalid_ticket_dates = support_tickets[
    support_tickets["resolved_at"].notna()
    & (
        support_tickets["resolved_at"]
        < support_tickets["created_at"]
    )
]

if len(invalid_ticket_dates) == 0:
    pass_check("Support resolution dates are valid")
else:
    fail_check(
        "Some support tickets were resolved before creation"
    )


# ---------------------------------------------------------
# FINAL RESULT
# ---------------------------------------------------------

print("\n---------------------------------")

if len(errors) == 0:

    print("ALL DATA VALIDATION CHECKS PASSED")

else:

    print(
        f"DATA VALIDATION FAILED: "
        f"{len(errors)} issue(s) found"
    )

    print("\nIssues:")

    for error in errors:
        print(f"- {error}")

print("---------------------------------\n")