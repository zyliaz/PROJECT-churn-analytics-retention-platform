# (1) Data Overview
- number of users: 8451 unique users in users table
- number of subscriptions: 7043 unique users in subscriptions table
- number of events: 21406796 events in user_events table
- key columns: 
	- users: gender, senior_citizen, has_partner, has_dependents
	- subscriptions: signup_date, cancel_date, plan, price, status, additional services included
	- user_events: event_time， device_type
- data ranges (Time range)
	- signup_date: 2023-01-01 00:00:00 to 2025-12-31 00:00:00
	- cancel_date: 2023-02-04 00:00:00 to 2025-12-31 00:00:00
	- event_time: 2023-01-01 00:00:19 to 2025-12-30 23:01:40

# (2) KPI Findings 
- churn distribution
	- mean      1.163714
	- min       0.220000
	- 50%       1.180000
	- max       2.290000
	- The churn rate increases dramatically at the begining, at local maximum at the end of the first year (2023), then drops the its lowest at end of second year (2024), then starts to increase again at the third year (2025). 
- retention initial insight
	- mean     98.836286
	- min      97.710000
	- 50%      98.820000
	- max      99.780000
	- The retention rate trend is the opposite of the churn rate, it peaks on 2024 and are at its lowest in 2023 and 2025. 
- active vs. cancelled count
	- active       5174
	- cancelled    1869

# (3) Events EDA Results
- event type proportions: 
	- cancel (8.8%)    188190
	- click (24.1%)    5159197
	- login (38.8%)    8310599
	- watch (36.2%)    7748810
- device mix
	- desktop (34.3%)    7338435
	- mobile (60.1%)    12873638
	- tablet (5.0%)     1087690
	- unknown (4.9%)     107033
- average events per user: 3,042
- early observations: 
	- login and watch are the most common event types
	- most people use mobile device

# (4) Potential Data Issues
- timestamp disorder: n/a, all cancel dates are after signup dates
- heavy users: some users have as high as 20498 events. 
- silent users: n/a, the lowest event number is 4

# (5) Next Step After Week 1
- build retention SQL
- build cohort table
- start funnel analysis
