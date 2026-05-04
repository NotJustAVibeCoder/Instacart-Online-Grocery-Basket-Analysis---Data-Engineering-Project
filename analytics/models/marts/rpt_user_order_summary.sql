select
  user_summary.user_id,
  user_summary.total_orders,
  user_summary.first_order_number,
  user_summary.latest_order_number,
  user_summary.avg_days_since_prior_order,
  count(distinct prior.order_id) as prior_orders_with_products,
  count(*) as prior_line_items,
  count(distinct prior.product_id) as unique_products_ordered,
  avg(prior.reordered) as reorder_rate
from {{ ref('int_user_order_summary') }} as user_summary
left join {{ ref('int_prior_order_details') }} as prior
  on user_summary.user_id = prior.user_id
group by
  user_summary.user_id,
  user_summary.total_orders,
  user_summary.first_order_number,
  user_summary.latest_order_number,
  user_summary.avg_days_since_prior_order
