

  create or replace view `instacart-basket-analysis`.`instacart_warehouse0371`.`stg_aisles`
  OPTIONS()
  as select aisle_id, aisle from `instacart-basket-analysis`.`instacart_warehouse0371`.`aisles_external`;

