select
  order_id,
  user_id,
  order_number,
  order_dow,
  order_hour_of_day,
  days_since_prior_order,
  product_id,
  product_name,
  aisle_id,
  aisle,
  department_id,
  department,
  add_to_cart_order,
  reordered
from {{ ref('int_prior_order_details') }}
