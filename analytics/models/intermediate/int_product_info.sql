select
  products.product_id,
  products.product_name,
  products.aisle_id,
  aisles.aisle,
  products.department_id,
  departments.department
from {{ ref('stg_products') }} as products
inner join {{ ref('stg_aisles') }} as aisles
  on products.aisle_id = aisles.aisle_id
inner join {{ ref('stg_departments') }} as departments
  on products.department_id = departments.department_id
