import random
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------

fake = Faker()
Faker.seed(42)
random.seed(42)

# Number of fictional customer companies
NUM_COMPANIES = 500

# Create data/generated folder automatically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 1. GENERATE SUBSCRIPTION PLANS
# ---------------------------------------------------------

plans = [
    {
        "plan_id": 1,
        "plan_name": "Starter",
        "monthly_price": 49.00,
        "max_users": 25,
        "storage_limit_gb": 50,
        "api_access": False,
        "ai_assistant_access": False,
        "workflow_automation_access": False,
        "created_at": datetime(2023, 1, 1),
        "is_active": True,
    },
    {
        "plan_id": 2,
        "plan_name": "Professional",
        "monthly_price": 199.00,
        "max_users": 150,
        "storage_limit_gb": 500,
        "api_access": True,
        "ai_assistant_access": True,
        "workflow_automation_access": True,
        "created_at": datetime(2023, 1, 1),
        "is_active": True,
    },
    {
        "plan_id": 3,
        "plan_name": "Enterprise",
        "monthly_price": 799.00,
        "max_users": 1000,
        "storage_limit_gb": 5000,
        "api_access": True,
        "ai_assistant_access": True,
        "workflow_automation_access": True,
        "created_at": datetime(2023, 1, 1),
        "is_active": True,
    },
]

plans_df = pd.DataFrame(plans)


# ---------------------------------------------------------
# 2. GENERATE CUSTOMER COMPANIES
# ---------------------------------------------------------

industries = [
    "Technology",
    "Healthcare",
    "Finance",
    "Retail",
    "Education",
    "Manufacturing",
    "Logistics",
]

countries = [
    "United States",
    "Canada",
    "United Kingdom",
    "Germany",
    "Australia",
    "India",
]

company_sizes = ["small", "medium", "enterprise"]

account_statuses = ["active", "trial", "suspended", "churned"]

companies = []

used_company_names = set()

for company_id in range(1, NUM_COMPANIES + 1):

    # Make sure every generated company name is unique
    company_name = fake.company()

    while company_name in used_company_names:
        company_name = fake.company()

    used_company_names.add(company_name)

    company_size = random.choices(
        company_sizes,
        weights=[55, 30, 15],
        k=1
    )[0]

    account_status = random.choices(
        account_statuses,
        weights=[72, 10, 5, 13],
        k=1
    )[0]

    created_at = fake.date_time_between(
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2026, 8, 1),
    )

    companies.append(
        {
            "company_id": company_id,
            "company_name": company_name,
            "industry": random.choice(industries),
            "country": random.choice(countries),
            "company_size": company_size,
            "created_at": created_at,
            "account_status": account_status,
        }
    )

companies_df = pd.DataFrame(companies)


# ---------------------------------------------------------
# 3. GENERATE USERS
# ---------------------------------------------------------

departments = [
    "Engineering",
    "Product",
    "Data",
    "Finance",
    "Marketing",
    "Sales",
    "Human Resources",
    "Operations",
]

job_roles = {
    "Engineering": ["Software Engineer", "Engineering Manager", "DevOps Engineer"],
    "Product": ["Product Manager", "Product Analyst", "Product Designer"],
    "Data": ["Data Analyst", "Data Scientist", "Analytics Manager"],
    "Finance": ["Financial Analyst", "Finance Manager", "Accountant"],
    "Marketing": ["Marketing Analyst", "Marketing Manager", "Growth Specialist"],
    "Sales": ["Account Executive", "Sales Manager", "Sales Representative"],
    "Human Resources": ["HR Specialist", "Recruiter", "HR Manager"],
    "Operations": ["Operations Analyst", "Operations Manager", "Coordinator"],
}

users = []
user_id = 1

for company in companies:

    # Larger companies generally have more Kraly users
    if company["company_size"] == "small":
        number_of_users = random.randint(3, 15)

    elif company["company_size"] == "medium":
        number_of_users = random.randint(15, 50)

    else:
        number_of_users = random.randint(50, 120)

    company_domain = (
        company["company_name"]
        .lower()
        .replace(" ", "")
        .replace(",", "")
        .replace(".", "")
        .replace("'", "")
        .replace("-", "")
    )

    for _ in range(number_of_users):

        first_name = fake.first_name()
        last_name = fake.last_name()

        department = random.choice(departments)
        job_role = random.choice(job_roles[department])

        signup_date = fake.date_between(
            start_date=company["created_at"].date(),
            end_date=datetime(2026, 8, 1).date(),
        )

        user_status = random.choices(
            ["active", "inactive", "deactivated"],
            weights=[82, 13, 5],
            k=1,
        )[0]

        email = (
            f"{first_name.lower()}.{last_name.lower()}.{user_id}"
            f"@{company_domain}.com"
        )

        users.append(
            {
                "user_id": user_id,
                "company_id": company["company_id"],
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "department": department,
                "job_role": job_role,
                "signup_date": signup_date,
                "user_status": user_status,
            }
        )

        user_id += 1

users_df = pd.DataFrame(users)


# ---------------------------------------------------------
# 4. GENERATE SUBSCRIPTIONS
# ---------------------------------------------------------

subscriptions = []
subscription_id = 1

for company in companies:

    if company["company_size"] == "small":
        plan_id = random.choices(
            [1, 2, 3],
            weights=[75, 23, 2],
            k=1,
        )[0]

    elif company["company_size"] == "medium":
        plan_id = random.choices(
            [1, 2, 3],
            weights=[15, 70, 15],
            k=1,
        )[0]

    else:
        plan_id = random.choices(
            [1, 2, 3],
            weights=[2, 28, 70],
            k=1,
        )[0]

    plan = plans[plan_id - 1]

    billing_cycle = random.choices(
        ["monthly", "annual"],
        weights=[65, 35],
        k=1,
    )[0]

    start_date = company["created_at"].date()

    # Subscription status should correspond with company status
    if company["account_status"] == "churned":
        subscription_status = "canceled"

        end_date = fake.date_between(
            start_date=start_date,
            end_date=datetime(2026, 8, 1).date(),
        )

        cancellation_reason = random.choice(
            [
                "Too expensive",
                "Missing required features",
                "Low product usage",
                "Switched to competitor",
                "Company downsizing",
                "Implementation challenges",
            ]
        )

    elif company["account_status"] == "trial":
        subscription_status = "trial"
        end_date = None
        cancellation_reason = None

    else:
        subscription_status = "active"
        end_date = None
        cancellation_reason = None

    # Count how many users belong to this company
    users_at_company = sum(
        1 for user in users
        if user["company_id"] == company["company_id"]
    )

    # Make sure the selected plan can support the company's users
    if users_at_company > plan["max_users"]:

        if users_at_company <= plans[1]["max_users"]:
            plan_id = 2  # Professional
        else:
            plan_id = 3  # Enterprise

        plan = plans[plan_id - 1]

    # Purchase enough seats for all current users,
    # plus some unused capacity for future growth
    max_extra_seats = min(
        20,
        plan["max_users"] - users_at_company
    )

    extra_seats = random.randint(0, max_extra_seats)

    seats_purchased = users_at_company + extra_seats

    # Simulate SaaS revenue based on base plan + seats
    extra_seat_revenue = seats_purchased * random.uniform(4, 9)

    monthly_recurring_revenue = round(
        plan["monthly_price"] + extra_seat_revenue,
        2,
    )

    subscriptions.append(
        {
            "subscription_id": subscription_id,
            "company_id": company["company_id"],
            "plan_id": plan_id,
            "start_date": start_date,
            "end_date": end_date,
            "billing_cycle": billing_cycle,
            "subscription_status": subscription_status,
            "seats_purchased": seats_purchased,
            "monthly_recurring_revenue": monthly_recurring_revenue,
            "cancellation_reason": cancellation_reason,
            "created_at": company["created_at"],
        }
    )

    subscription_id += 1

subscriptions_df = pd.DataFrame(subscriptions)


# ---------------------------------------------------------
# 5. GENERATE PROJECTS
# ---------------------------------------------------------

projects = []
project_id = 1

# Group users by company so we can easily select valid users
users_by_company = {}

for user in users:
    users_by_company.setdefault(user["company_id"], []).append(user)


for company in companies:

    company_users = users_by_company[company["company_id"]]

    # Larger companies generally create more projects.
    # Churned/trial companies generally have less activity.
    if company["company_size"] == "small":
        number_of_projects = random.randint(2, 8)

    elif company["company_size"] == "medium":
        number_of_projects = random.randint(6, 18)

    else:
        number_of_projects = random.randint(15, 35)

    if company["account_status"] == "churned":
        number_of_projects = max(
            1,
            int(number_of_projects * random.uniform(0.3, 0.6))
        )

    elif company["account_status"] == "trial":
        number_of_projects = max(
            1,
            int(number_of_projects * random.uniform(0.2, 0.5))
        )

    for project_number in range(1, number_of_projects + 1):

        creator = random.choice(company_users)

        project_created_at = fake.date_time_between(
            start_date=company["created_at"],
            end_date=datetime(2026, 8, 1),
        )

        project_status = random.choices(
            ["planned", "active", "completed", "archived"],
            weights=[10, 40, 40, 10],
            k=1,
        )[0]

        priority = random.choices(
            ["low", "medium", "high", "urgent"],
            weights=[15, 50, 28, 7],
            k=1,
        )[0]

        due_date = (
            project_created_at
            + timedelta(days=random.randint(14, 180))
        ).date()

        if project_status == "completed":
            completed_at = (
                project_created_at
                + timedelta(days=random.randint(7, 120))
            )

            # Don't allow completion after our dataset cutoff
            if completed_at > datetime(2026, 8, 1):
                completed_at = datetime(2026, 8, 1)

        else:
            completed_at = None

        projects.append(
            {
                "project_id": project_id,
                "company_id": company["company_id"],
                "created_by_user_id": creator["user_id"],
                "project_name": f"{fake.bs().title()} Project",
                "project_description": fake.sentence(nb_words=10),
                "created_at": project_created_at,
                "due_date": due_date,
                "completed_at": completed_at,
                "project_status": project_status,
                "priority": priority,
            }
        )

        project_id += 1

projects_df = pd.DataFrame(projects)


# ---------------------------------------------------------
# 6. GENERATE TASKS
# ---------------------------------------------------------

tasks = []
task_id = 1

for project in projects:

    company_users = users_by_company[project["company_id"]]

    number_of_tasks = random.randint(5, 25)

    for task_number in range(1, number_of_tasks + 1):

        creator = random.choice(company_users)

        # Most tasks are assigned, but some remain unassigned.
        assigned_user = random.choice(company_users)

        if random.random() < 0.05:
            assigned_user_id = None
        else:
            assigned_user_id = assigned_user["user_id"]

        task_created_at = fake.date_time_between(
            start_date=project["created_at"],
            end_date=datetime(2026, 8, 1),
        )

        task_status = random.choices(
            ["open", "in progress", "completed", "canceled"],
            weights=[20, 25, 50, 5],
            k=1,
        )[0]

        priority = random.choices(
            ["low", "medium", "high", "urgent"],
            weights=[20, 50, 25, 5],
            k=1,
        )[0]

        due_date = (
            task_created_at
            + timedelta(days=random.randint(1, 45))
        ).date()

        if task_status == "completed":

            completed_at = (
                task_created_at
                + timedelta(days=random.randint(1, 30))
            )

            if completed_at > datetime(2026, 8, 1):
                completed_at = datetime(2026, 8, 1)

        else:
            completed_at = None

        tasks.append(
            {
                "task_id": task_id,
                "project_id": project["project_id"],
                "assigned_user_id": assigned_user_id,
                "created_by_user_id": creator["user_id"],
                "task_name": fake.catch_phrase(),
                "task_description": fake.sentence(nb_words=12),
                "priority": priority,
                "created_at": task_created_at,
                "due_date": due_date,
                "completed_at": completed_at,
                "task_status": task_status,
            }
        )

        task_id += 1

tasks_df = pd.DataFrame(tasks)


# ---------------------------------------------------------
# 7. GENERATE SUPPORT TICKETS
# ---------------------------------------------------------

support_categories = [
    "Billing",
    "Technical issue",
    "Account access",
    "Feature request",
    "Performance",
    "Other",
]

support_tickets = []
ticket_id = 1

for company in companies:

    company_users = users_by_company[company["company_id"]]

    # Customers with problems/churn generate more support tickets.
    if company["account_status"] == "churned":
        number_of_tickets = random.randint(8, 20)

    elif company["account_status"] == "suspended":
        number_of_tickets = random.randint(6, 15)

    elif company["account_status"] == "trial":
        number_of_tickets = random.randint(1, 5)

    else:
        number_of_tickets = random.randint(2, 10)

    for _ in range(number_of_tickets):

        submitter = random.choice(company_users)

        created_at = fake.date_time_between(
            start_date=company["created_at"],
            end_date=datetime(2026, 8, 1),
        )

        priority = random.choices(
            ["low", "medium", "high", "urgent"],
            weights=[20, 50, 25, 5],
            k=1,
        )[0]

        ticket_status = random.choices(
            ["open", "pending", "resolved", "closed"],
            weights=[10, 10, 45, 35],
            k=1,
        )[0]

        # Higher-priority issues generally receive faster first responses.
        if priority == "urgent":
            response_hours = random.uniform(0.1, 2)

        elif priority == "high":
            response_hours = random.uniform(1, 6)

        elif priority == "medium":
            response_hours = random.uniform(2, 18)

        else:
            response_hours = random.uniform(4, 36)

        first_response_at = (
            created_at
            + timedelta(hours=response_hours)
        )

        if first_response_at > datetime(2026, 8, 1):
            first_response_at = None

        if ticket_status in ["resolved", "closed"]:

            resolution_hours = random.uniform(4, 120)

            resolved_at = (
                created_at
                + timedelta(hours=resolution_hours)
            )

            if resolved_at > datetime(2026, 8, 1):
                resolved_at = datetime(2026, 8, 1)

            # Churned customers tend to report somewhat lower satisfaction.
            if company["account_status"] == "churned":

                satisfaction_score = random.choices(
                    [1, 2, 3, 4, 5],
                    weights=[25, 30, 25, 15, 5],
                    k=1,
                )[0]

            else:

                satisfaction_score = random.choices(
                    [1, 2, 3, 4, 5],
                    weights=[5, 10, 20, 35, 30],
                    k=1,
                )[0]

        else:
            resolved_at = None
            satisfaction_score = None

        support_tickets.append(
            {
                "ticket_id": ticket_id,
                "company_id": company["company_id"],
                "submitted_by_user_id": submitter["user_id"],
                "category": random.choice(support_categories),
                "priority": priority,
                "subject": fake.sentence(nb_words=6),
                "description": fake.sentence(nb_words=15),
                "created_at": created_at,
                "first_response_at": first_response_at,
                "resolved_at": resolved_at,
                "ticket_status": ticket_status,
                "satisfaction_score": satisfaction_score,
            }
        )

        ticket_id += 1

support_tickets_df = pd.DataFrame(support_tickets)


# ---------------------------------------------------------
# 8. GENERATE LOGIN EVENTS
# ---------------------------------------------------------

login_events = []
login_event_id = 1

company_status_lookup = {
    company["company_id"]: company["account_status"]
    for company in companies
}

DATA_END_DATE = datetime(2026, 8, 1)

for user in users:

    company_status = company_status_lookup[user["company_id"]]

    # Determine activity level based on user/company status
    if user["user_status"] == "deactivated":
        number_of_logins = random.randint(0, 3)

    elif user["user_status"] == "inactive":
        number_of_logins = random.randint(2, 8)

    elif company_status == "churned":
        number_of_logins = random.randint(3, 10)

    elif company_status == "trial":
        number_of_logins = random.randint(5, 15)

    else:
        number_of_logins = random.randint(10, 25)

    signup_datetime = datetime.combine(
        user["signup_date"],
        datetime.min.time()
    )

    for _ in range(number_of_logins):

        login_timestamp = fake.date_time_between(
            start_date=signup_datetime,
            end_date=DATA_END_DATE,
        )

        login_successful = random.choices(
            [True, False],
            weights=[96, 4],
            k=1,
        )[0]

        device_type = random.choices(
            ["desktop", "mobile", "tablet"],
            weights=[70, 25, 5],
            k=1,
        )[0]

        operating_system = random.choice(
            ["Windows", "macOS", "Linux", "iOS", "Android"]
        )

        if login_successful:

            session_duration_minutes = random.randint(5, 180)

            logout_timestamp = (
                login_timestamp
                + timedelta(minutes=session_duration_minutes)
            )

            failure_reason = None

        else:

            session_duration_minutes = None
            logout_timestamp = None

            failure_reason = random.choice(
                [
                    "Invalid password",
                    "Account locked",
                    "Expired session",
                    "MFA failure",
                ]
            )

        login_events.append(
            {
                "login_event_id": login_event_id,
                "user_id": user["user_id"],
                "login_timestamp": login_timestamp,
                "logout_timestamp": logout_timestamp,
                "session_duration_minutes": session_duration_minutes,
                "device_type": device_type,
                "operating_system": operating_system,
                "login_successful": login_successful,
                "failure_reason": failure_reason,
            }
        )

        login_event_id += 1

login_events_df = pd.DataFrame(login_events)


# ---------------------------------------------------------
# 9. GENERATE FEATURE USAGE EVENTS
# ---------------------------------------------------------

features = [
    "Task Management",
    "Project Dashboard",
    "Reporting",
    "Team Collaboration",
    "File Storage",
    "API",
    "AI Assistant",
    "Workflow Automation",
]

event_names = [
    "viewed",
    "created",
    "updated",
    "completed",
    "exported",
]

feature_usage_events = []
feature_event_id = 1

# Map projects to companies
projects_by_company = {}

for project in projects:
    projects_by_company.setdefault(
        project["company_id"], []
    ).append(project)


for login in login_events:

    # Failed logins don't produce feature activity
    if not login["login_successful"]:
        continue

    user = users[login["user_id"] - 1]

    company_id = user["company_id"]
    company_status = company_status_lookup[company_id]

    # Each successful session generates several feature interactions
    if company_status == "churned":
        number_of_events = random.randint(1, 2)

    elif user["user_status"] == "inactive":
        number_of_events = random.randint(1, 2)

    else:
        number_of_events = random.randint(1, 4)

    session_id = f"SESSION-{login['login_event_id']:08d}"

    company_projects = projects_by_company.get(
        company_id,
        []
    )

    for _ in range(number_of_events):

        feature_name = random.choice(features)

        # Some features are usually associated with a project
        if (
            company_projects
            and feature_name
            in [
                "Task Management",
                "Project Dashboard",
                "Team Collaboration",
                "File Storage",
            ]
        ):
            project_id_value = random.choice(
                company_projects
            )["project_id"]

        else:
            project_id_value = None

        event_timestamp = (
            login["login_timestamp"]
            + timedelta(
                minutes=random.randint(
                    0,
                    max(
                        1,
                        login["session_duration_minutes"]
                    )
                )
            )
        )

        feature_usage_events.append(
            {
                "feature_event_id": feature_event_id,
                "user_id": user["user_id"],
                "company_id": company_id,
                "feature_name": feature_name,
                "event_name": random.choice(event_names),
                "event_timestamp": event_timestamp,
                "session_id": session_id,
                "project_id": project_id_value,
                "usage_count": random.randint(1, 5),
            }
        )

        feature_event_id += 1

feature_usage_events_df = pd.DataFrame(
    feature_usage_events
)


# ---------------------------------------------------------
# 10. GENERATE INVOICES
# ---------------------------------------------------------

invoices = []
invoice_id = 1

for subscription in subscriptions:

    subscription_start = subscription["start_date"]

    if subscription["end_date"] is not None:
        subscription_end = subscription["end_date"]
    else:
        subscription_end = DATA_END_DATE.date()

    billing_date = subscription_start

    while billing_date <= subscription_end:

        billing_period_start = billing_date

        billing_period_end = (
            billing_date + timedelta(days=29)
        )

        if billing_period_end > subscription_end:
            billing_period_end = subscription_end

        subtotal = round(
            subscription["monthly_recurring_revenue"],
            2
        )

        discount_amount = round(
            subtotal
            * random.choices(
                [0, 0.05, 0.10],
                weights=[80, 12, 8],
                k=1,
            )[0],
            2,
        )

        taxable_amount = subtotal - discount_amount

        tax_amount = round(
            taxable_amount
            * random.uniform(0.00, 0.10),
            2,
        )

        amount_due = round(
            taxable_amount + tax_amount,
            2,
        )

        due_date = (
            billing_date
            + timedelta(days=30)
        )

        company_status = company_status_lookup[
            subscription["company_id"]
        ]

        if company_status == "churned":

            invoice_status = random.choices(
                ["paid", "overdue", "canceled"],
                weights=[55, 35, 10],
                k=1,
            )[0]

        elif company_status == "suspended":

            invoice_status = random.choices(
                ["paid", "overdue"],
                weights=[55, 45],
                k=1,
            )[0]

        else:

            invoice_status = random.choices(
                ["paid", "overdue", "pending"],
                weights=[88, 7, 5],
                k=1,
            )[0]

        invoices.append(
            {
                "invoice_id": invoice_id,
                "company_id": subscription["company_id"],
                "subscription_id": subscription["subscription_id"],
                "invoice_date": billing_date,
                "billing_period_start": billing_period_start,
                "billing_period_end": billing_period_end,
                "due_date": due_date,
                "subtotal": subtotal,
                "tax_amount": tax_amount,
                "discount_amount": discount_amount,
                "amount_due": amount_due,
                "invoice_status": invoice_status,
            }
        )

        invoice_id += 1

        # Move approximately one month forward
        billing_date = (
            billing_date
            + timedelta(days=30)
        )

invoices_df = pd.DataFrame(invoices)


# ---------------------------------------------------------
# 11. GENERATE PAYMENTS
# ---------------------------------------------------------

payments = []
payment_id = 1

payment_methods = [
    "card",
    "ACH",
    "wire transfer",
]

for invoice in invoices:

    # Pending/canceled invoices may not have a payment record
    if invoice["invoice_status"] in [
        "pending",
        "canceled",
    ]:
        continue

    if invoice["invoice_status"] == "paid":

        payment_status = random.choices(
            ["successful", "refunded"],
            weights=[97, 3],
            k=1,
        )[0]

    else:

        payment_status = random.choices(
            ["failed", "pending"],
            weights=[80, 20],
            k=1,
        )[0]

    payment_date = (
        invoice["invoice_date"]
        + timedelta(days=random.randint(0, 35))
    )

    if payment_status in ["successful", "refunded"]:

        amount_paid = invoice["amount_due"]
        failure_reason = None

    else:

        amount_paid = 0

        failure_reason = random.choice(
            [
                "Insufficient funds",
                "Card declined",
                "Expired card",
                "Bank rejected payment",
            ]
        )

    if payment_status == "refunded":

        refunded_at = (
            payment_date
            + timedelta(days=random.randint(1, 30))
        )

    else:
        refunded_at = None

    payments.append(
        {
            "payment_id": payment_id,
            "invoice_id": invoice["invoice_id"],
            "payment_date": payment_date,
            "amount_paid": amount_paid,
            "payment_method": random.choice(payment_methods),
            "payment_status": payment_status,
            "transaction_reference": (
                f"TXN-{payment_id:010d}"
            ),
            "failure_reason": failure_reason,
            "refunded_at": refunded_at,
        }
    )

    payment_id += 1

payments_df = pd.DataFrame(payments)


# ---------------------------------------------------------
# 8. SAVE GENERATED DATA
# ---------------------------------------------------------

plans_df.to_csv(OUTPUT_DIR / "plans.csv", index=False)

companies_df.to_csv(OUTPUT_DIR / "companies.csv", index=False)

users_df.to_csv(OUTPUT_DIR / "users.csv", index=False)

subscriptions_df.to_csv(
    OUTPUT_DIR / "subscriptions.csv",
    index=False
)

projects_df.to_csv(
    OUTPUT_DIR / "projects.csv",
    index=False
)

tasks_df.to_csv(
    OUTPUT_DIR / "tasks.csv",
    index=False
)

support_tickets_df.to_csv(
    OUTPUT_DIR / "support_tickets.csv",
    index=False
)

login_events_df.to_csv(
    OUTPUT_DIR / "login_events.csv",
    index=False
)

feature_usage_events_df.to_csv(
    OUTPUT_DIR / "feature_usage_events.csv",
    index=False
)

invoices_df.to_csv(
    OUTPUT_DIR / "invoices.csv",
    index=False
)

payments_df.to_csv(
    OUTPUT_DIR / "payments.csv",
    index=False
)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print("\nSynthetic SaaS data generated successfully!")
print("-------------------------------------------")
print(f"Plans:         {len(plans_df):,}")
print(f"Companies:     {len(companies_df):,}")
print(f"Users:         {len(users_df):,}")
print(f"Subscriptions: {len(subscriptions_df):,}")
print(f"Projects:      {len(projects_df):,}")
print(f"Tasks:         {len(tasks_df):,}")
print(f"Support:       {len(support_tickets_df):,}")
print(f"Login Events:  {len(login_events_df):,}")
print(f"Feature Usage: {len(feature_usage_events_df):,}")
print(f"Invoices:      {len(invoices_df):,}")
print(f"Payments:      {len(payments_df):,}")

print(f"\nFiles saved to:")
print(OUTPUT_DIR)