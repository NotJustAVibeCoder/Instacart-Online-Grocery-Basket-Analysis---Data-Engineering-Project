select
  department_id,
  department
from {{ source('instacart_raw', 'departments_external') }}
