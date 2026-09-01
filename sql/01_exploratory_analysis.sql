-- ============================================================
-- KRALY SaaS ANALYTICS
-- 01 - EXPLORATORY DATA ANALYSIS
-- ============================================================


-- 1. Customer count
SELECT COUNT(*) AS total_companies
FROM companies;


-- 2. Companies by account status
SELECT
    account_status,
    COUNT(*) AS company_count
FROM companies
GROUP BY account_status
ORDER BY company_count DESC;


-- 3. Companies by industry
SELECT
    industry,
    COUNT(*) AS company_count
FROM companies
GROUP BY industry
ORDER BY company_count DESC;


-- 4. Companies by size
SELECT
    company_size,
    COUNT(*) AS company_count
FROM companies
GROUP BY company_size
ORDER BY company_count DESC;


-- 5. Users by status
SELECT
    user_status,
    COUNT(*) AS user_count
FROM users
GROUP BY user_status
ORDER BY user_count DESC;


-- 6. Customers by subscription plan
SELECT
    p.plan_name,
    COUNT(*) AS subscriptions
FROM subscriptions s
JOIN plans p
    ON s.plan_id = p.plan_id
GROUP BY p.plan_name
ORDER BY subscriptions DESC;


-- 7. Subscription status distribution
SELECT
    subscription_status,
    COUNT(*) AS subscriptions
FROM subscriptions
GROUP BY subscription_status
ORDER BY subscriptions DESC;


-- 8. Total projects
SELECT COUNT(*) AS total_projects
FROM projects;


-- 9. Projects by status
SELECT
    project_status,
    COUNT(*) AS project_count
FROM projects
GROUP BY project_status
ORDER BY project_count DESC;


-- 10. Tasks by status
SELECT
    task_status,
    COUNT(*) AS task_count
FROM tasks
GROUP BY task_status
ORDER BY task_count DESC;