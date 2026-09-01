CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) UNIQUE NOT NULL,
    industry VARCHAR(50) NOT NULL,
    country VARCHAR(75) NOT NULL,
    company_size VARCHAR(20) NOT NULL
        CHECK (company_size IN ('small', 'medium', 'enterprise')),
    created_at TIMESTAMP NOT NULL,
    account_status VARCHAR(20) NOT NULL
        CHECK (account_status IN ('trial', 'active', 'suspended', 'churned'))
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    job_role VARCHAR(75) NOT NULL,
    signup_date DATE NOT NULL,
    user_status VARCHAR(20) NOT NULL
        CHECK (user_status IN ('active', 'inactive', 'deactivated')),

    CONSTRAINT fk_users_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    plan_name VARCHAR(30) UNIQUE NOT NULL
        CHECK (plan_name IN ('Starter', 'Professional', 'Enterprise')),
    monthly_price NUMERIC(10,2) NOT NULL
        CHECK (monthly_price >= 0),
    max_users INTEGER NOT NULL
        CHECK (max_users > 0),
    storage_limit_gb INTEGER NOT NULL
        CHECK (storage_limit_gb > 0),
    api_access BOOLEAN NOT NULL,
    ai_assistant_access BOOLEAN NOT NULL,
    workflow_automation_access BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL
);

CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    billing_cycle VARCHAR(20) NOT NULL
        CHECK (billing_cycle IN ('monthly', 'annual')),
    subscription_status VARCHAR(20) NOT NULL
        CHECK (subscription_status IN ('trial', 'active', 'canceled', 'expired')),
    seats_purchased INTEGER NOT NULL
        CHECK (seats_purchased > 0),
    monthly_recurring_revenue NUMERIC(12,2) NOT NULL
        CHECK (monthly_recurring_revenue >= 0),
    cancellation_reason VARCHAR(150),
    created_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_subscriptions_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id),

    CONSTRAINT fk_subscriptions_plan
        FOREIGN KEY (plan_id)
        REFERENCES plans(plan_id),

    CONSTRAINT chk_subscription_dates
        CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    created_by_user_id INTEGER NOT NULL,
    project_name VARCHAR(150) NOT NULL,
    project_description TEXT,
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    completed_at TIMESTAMP,
    project_status VARCHAR(20) NOT NULL
        CHECK (project_status IN ('planned', 'active', 'completed', 'archived')),
    priority VARCHAR(20) NOT NULL
        CHECK (priority IN ('low', 'medium', 'high', 'urgent')),

    CONSTRAINT fk_projects_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id),

    CONSTRAINT fk_projects_creator
        FOREIGN KEY (created_by_user_id)
        REFERENCES users(user_id)
);

CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    assigned_user_id INTEGER,
    created_by_user_id INTEGER NOT NULL,
    task_name VARCHAR(150) NOT NULL,
    task_description TEXT,
    priority VARCHAR(20) NOT NULL
        CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    completed_at TIMESTAMP,
    task_status VARCHAR(20) NOT NULL
        CHECK (task_status IN ('open', 'in progress', 'completed', 'canceled')),

    CONSTRAINT fk_tasks_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id),

    CONSTRAINT fk_tasks_assignee
        FOREIGN KEY (assigned_user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_tasks_creator
        FOREIGN KEY (created_by_user_id)
        REFERENCES users(user_id)
);

CREATE TABLE login_events (
    login_event_id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    login_timestamp TIMESTAMP NOT NULL,
    logout_timestamp TIMESTAMP,
    session_duration_minutes INTEGER
        CHECK (session_duration_minutes >= 0),
    device_type VARCHAR(20)
        CHECK (device_type IN ('desktop', 'mobile', 'tablet')),
    operating_system VARCHAR(30),
    login_successful BOOLEAN NOT NULL,
    failure_reason VARCHAR(100),

    CONSTRAINT fk_login_events_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE feature_usage_events (
    feature_event_id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    project_id INTEGER,
    feature_name VARCHAR(75) NOT NULL,
    event_name VARCHAR(75) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    session_id VARCHAR(100),
    usage_count INTEGER NOT NULL
        CHECK (usage_count > 0),

    CONSTRAINT fk_feature_usage_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_feature_usage_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id),

    CONSTRAINT fk_feature_usage_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
);

CREATE TABLE support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    submitted_by_user_id INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL
        CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    subject VARCHAR(150),
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    first_response_at TIMESTAMP,
    resolved_at TIMESTAMP,
    ticket_status VARCHAR(20)
        CHECK (ticket_status IN ('open', 'pending', 'resolved', 'closed')),
    satisfaction_score INTEGER
        CHECK (satisfaction_score BETWEEN 1 AND 5),

    CONSTRAINT fk_support_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id),

    CONSTRAINT fk_support_user
        FOREIGN KEY (submitted_by_user_id)
        REFERENCES users(user_id)
);

CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    subscription_id INTEGER NOT NULL,
    invoice_date DATE NOT NULL,
    billing_period_start DATE,
    billing_period_end DATE,
    due_date DATE,
    subtotal NUMERIC(12,2)
        CHECK (subtotal >= 0),
    tax_amount NUMERIC(12,2)
        CHECK (tax_amount >= 0),
    discount_amount NUMERIC(12,2)
        CHECK (discount_amount >= 0),
    amount_due NUMERIC(12,2)
        CHECK (amount_due >= 0),
    invoice_status VARCHAR(20)
        CHECK (invoice_status IN ('pending', 'paid', 'overdue', 'canceled')),

    CONSTRAINT fk_invoices_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id),

    CONSTRAINT fk_invoices_subscription
        FOREIGN KEY (subscription_id)
        REFERENCES subscriptions(subscription_id)
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    payment_date TIMESTAMP NOT NULL,
    amount_paid NUMERIC(12,2) NOT NULL
        CHECK (amount_paid >= 0),
    payment_method VARCHAR(30)
        CHECK (payment_method IN ('card', 'ACH', 'wire transfer')),
    payment_status VARCHAR(20)
        CHECK (payment_status IN ('successful', 'failed', 'pending', 'refunded')),
    transaction_reference VARCHAR(100) UNIQUE,
    failure_reason VARCHAR(100),
    refunded_at TIMESTAMP,

    CONSTRAINT fk_payments_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(invoice_id)
);