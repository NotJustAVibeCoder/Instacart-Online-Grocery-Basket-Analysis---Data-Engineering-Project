select
  product_id,
  product_name,
  aisle_id,
  aisle,
  department_id,
  department
from {{ ref('int_product_info') }}
