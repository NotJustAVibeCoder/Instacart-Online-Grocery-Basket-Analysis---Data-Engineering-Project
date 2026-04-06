select
  order_id,
  user_id,
  eval_set,
  order_number,
  order_dow,
  order_hour_of_day,
  days_since_prior_order
from {{ source('instacart_raw', 'orders_external') }}
