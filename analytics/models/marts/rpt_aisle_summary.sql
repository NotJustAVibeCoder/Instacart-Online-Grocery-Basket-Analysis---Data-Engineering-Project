select
  aisle_id,
  aisle,
  department_id,
  department,
  count(*) as line_items,
  count(distinct order_id) as orders,
  count(distinct user_id) as users,
  count(distinct product_id) as products,
  avg(reordered) as reorder_rate,
  avg(add_to_cart_order) as avg_add_to_cart_position
from {{ ref('fct_prior_order_lines') }}
group by aisle_id, aisle, department_id, department
