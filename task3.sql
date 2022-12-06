SELECT
    base.month_installed,
    IFNULL(cohort.days_diff, 0) as days_diff,
    IFNULL(cohort.users_per_day, 0) / base.users as retention_rate
FROM
    (SELECT 
        DATE_FORMAT(user.installed_at, '%Y.%m') as month_installed,
        COUNT(DISTINCT user.user_id) as users
    FROM USER as user
    GROUP BY 
        DATE_FORMAT(user.installed_at, '%Y.%m')
    ) as base
LEFT JOIN
    (SELECT DATE_FORMAT(user.installed_at, '%Y.%m') as month_installed,
        DATEDIFF(cs.created_at,  user.installed_at) as days_diff,
        COUNT(DISTINCT user.user_id) as users_per_day
    FROM USER as user
    LEFT JOIN CLIENT_SESSION as cs ON cs.user_id = user.user_id
    WHERE DATEDIFF(cs.created_at,  user.installed_at) IN (1, 3, 7)
    GROUP BY 
        DATE_FORMAT(user.installed_at, '%Y.%m'),
        DATEDIFF(cs.created_at,  user.installed_at)
    ) as cohort on base.month_installed = cohort.month_installed
ORDER BY 
    base.month_installed,
    cohort.days_diff
