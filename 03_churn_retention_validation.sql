# active users at beginning of the month #
WITH month_list AS (
    SELECT DISTINCT DATE_FORMAT(signup_date, '%Y-%m-01') AS month_in_list
    FROM subscriptions
    WHERE signup_date IS NOT NULL
    UNION
    SELECT DISTINCT DATE_FORMAT(cancel_date, '%Y-%m-01') AS month_in_list
    FROM subscriptions
    WHERE cancel_date IS NOT NULL
)
SELECT
    DATE_FORMAT(m.month_start, '%Y-%m') AS month,
    COUNT(DISTINCT s.user_id) AS active_users_at_start
FROM month_list m
CROSS JOIN subscriptions s
WHERE s.signup_date <= LAST_DAY(DATE_SUB(m.month_start, INTERVAL 1 DAY))
  AND (s.cancel_date IS NULL OR s.cancel_date >= m.month_start)
GROUP BY m.month_start
ORDER BY m.month_start;

# monthly churn rate (= churn count in that month / active users at beginning of the month)
SELECT
	month,
    churn_users/active_users_at_start as monthly_churn_rate
FROM
	(WITH month_list AS (
		SELECT DISTINCT DATE_FORMAT(signup_date, '%Y-%m-01') AS month_start
		FROM subscriptions
		WHERE signup_date IS NOT NULL
		UNION
		SELECT DISTINCT DATE_FORMAT(cancel_date, '%Y-%m-01') AS month_start
		FROM subscriptions
		WHERE cancel_date IS NOT NULL
	)
	SELECT 
		m.month_start,
		DATE_FORMAT(m.month_start, '%Y-%m') AS month,
		COUNT(DISTINCT s.user_id) AS active_users_at_start
	FROM month_list m
	CROSS JOIN subscriptions s
	WHERE s.signup_date <= LAST_DAY(DATE_SUB(m.month_start, INTERVAL 1 DAY))
	  AND (s.cancel_date IS NULL OR s.cancel_date >= m.month_start)
	GROUP BY m.month_start
	ORDER BY m.month_start) AS active_users
JOIN 
	(SELECT 
			DATE_FORMAT(cancel_date, '%Y-%m') AS cancel_month, 
			COUNT(*) AS churn_users
		FROM subscriptions
		WHERE cancel_date IS NOT NULL
		GROUP BY 1
	) AS churn_count
ON active_users.month = churn_count.cancel_month
ORDER BY month;

-- 
WITH active_at_start AS (
    WITH month_list AS (
    SELECT DISTINCT DATE_FORMAT(signup_date, '%Y-%m-01') AS month_start
    FROM subscriptions
    WHERE signup_date IS NOT NULL
    UNION
    SELECT DISTINCT DATE_FORMAT(cancel_date, '%Y-%m-01') AS month_start
    FROM subscriptions
    WHERE cancel_date IS NOT NULL
)
SELECT 
    DATE_FORMAT(m.month_start, '%Y-%m') AS month,
    COUNT(DISTINCT s.user_id) AS active_users
FROM month_list m
CROSS JOIN subscriptions s
WHERE s.signup_date <= LAST_DAY(DATE_SUB(m.month_start, INTERVAL 1 DAY))
  AND (s.cancel_date IS NULL OR s.cancel_date >= m.month_start)
GROUP BY m.month_start
ORDER BY m.month_start)
, churned_in_month AS (
    SELECT 
		DATE_FORMAT(cancel_date, '%Y-%m') AS month, 
		COUNT(*) AS churned_users
	FROM subscriptions
	WHERE cancel_date IS NOT NULL
	GROUP BY 1
	)
SELECT 
    COALESCE(a.month, c.month) AS month,
    COALESCE(a.active_users, 0) AS active_users_at_start,
    COALESCE(c.churned_users, 0) AS churned_users,
    CASE 
        WHEN COALESCE(a.active_users, 0) > 0 
        THEN ROUND(COALESCE(c.churned_users, 0) * 100.0 / a.active_users, 2)
        ELSE 0 
    END AS churn_rate_percentage
FROM active_at_start a
LEFT JOIN churned_in_month c 
	ON a.month = c.month;
UNION
(SELECT 
    c.month,
    active_users_at_start,
    c.churned_users,
    churn_rate_percentage
FROM churned_in_month c
WHERE c.month NOT IN (SELECT month FROM active_at_start)
ORDER BY month);



# retention rate (= 1 - Monthly Churn Rate)
WITH active_at_start AS (
    WITH month_list AS (
		SELECT DISTINCT DATE_FORMAT(signup_date, '%Y-%m-01') AS month_start
		FROM subscriptions
		WHERE signup_date IS NOT NULL
		UNION
		SELECT DISTINCT DATE_FORMAT(cancel_date, '%Y-%m-01') AS month_start
		FROM subscriptions
		WHERE cancel_date IS NOT NULL
	)
	SELECT 
		DATE_FORMAT(m.month_start, '%Y-%m') AS month,
		COUNT(DISTINCT s.user_id) AS active_users
	FROM month_list m
	CROSS JOIN subscriptions s
	WHERE s.signup_date <= LAST_DAY(DATE_SUB(m.month_start, INTERVAL 1 DAY))
	  AND (s.cancel_date IS NULL OR s.cancel_date >= m.month_start)
	GROUP BY m.month_start
),
churned_in_month AS (
    SELECT
        DATE_FORMAT(cancel_date, '%Y-%m') AS month,
        COUNT(*) AS churned_users
    FROM subscriptions
    WHERE cancel_date IS NOT NULL
    GROUP BY DATE_FORMAT(cancel_date, '%Y-%m')
),
retained_in_month AS (
    SELECT 
        a.month,
        a.active_users AS active_at_start,
        COALESCE(c.churned_users, 0) AS churned,
        a.active_users - COALESCE(c.churned_users, 0) AS retained_users
    FROM active_at_start a
    LEFT JOIN churned_in_month c ON a.month = c.month
)
SELECT 
    month,
    active_at_start,
    churned,
    retained_users,
    CASE 
        WHEN active_at_start > 0 
        THEN ROUND(retained_users * 100.0 / active_at_start, 2)
        ELSE 0 
    END AS retention_rate_percentage,
    CASE 
        WHEN active_at_start > 0 
        THEN ROUND(churned * 100.0 / active_at_start, 2)
        ELSE 0 
    END AS churn_rate_percentage
FROM retained_in_month
ORDER BY month;