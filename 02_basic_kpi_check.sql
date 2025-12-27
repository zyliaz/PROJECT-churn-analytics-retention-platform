USE churn_analytics;

# total users #
select
	count(*) as total_users
from users;
#######################################

# total subscriptions #
select
	count(*) as subscribed_users
from subscriptions;
#######################################

# activly subscribed and cancelled users #
select
	status,
    count(*) as users
from subscriptions
group by status;
#######################################

# monthly churn count #
select
	date_format(cancel_date, '%Y-%m') as cancel_month,
    count(*) as churn_users
from subscriptions
where cancel_date is not null
group by cancel_month
order by cancel_month;
