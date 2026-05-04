select
  user_id,
  count(*) as total_orders,
  min(order_number) as first_order_number,
  max(order_number) as latest_order_number,
  avg(days_since_prior_order) as avg_days_since_prior_order
from {{ ref('stg_orders') }}
group by user_id
