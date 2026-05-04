select
  prior.order_id,
  orders.user_id,
  orders.order_number,
  orders.order_dow,
  orders.order_hour_of_day,
  orders.days_since_prior_order,
  prior.product_id,
  product_info.product_name,
  product_info.aisle_id,
  product_info.aisle,
  product_info.department_id,
  product_info.department,
  prior.add_to_cart_order,
  prior.reordered
from {{ ref('stg_order_products_prior') }} as prior
inner join {{ ref('stg_orders') }} as orders
  on prior.order_id = orders.order_id
inner join {{ ref('int_product_info') }} as product_info
  on prior.product_id = product_info.product_id
