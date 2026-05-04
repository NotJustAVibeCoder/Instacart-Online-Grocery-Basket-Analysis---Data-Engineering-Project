from __future__ import annotations

import os

from google.cloud import bigquery


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def create_table_bigquery_sql(table_names, dataset_id, project_id, bucket_name, bucket_prefix=""):
    client = bigquery.Client(project=project_id)

    for table_name in table_names:
        object_path = f"{bucket_prefix.rstrip('/')}/{table_name}.csv" if bucket_prefix else f"instacart_raw/{table_name}.csv"
        create_table_sql = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{project_id}.{dataset_id}.{table_name}_external`
        OPTIONS (
          format = 'CSV',
          uris = [
            'gs://{bucket_name}/{object_path}'
          ]
        );
        """
        job = client.query(create_table_sql)
        job.result()
        print(f"Created/updated external table: {project_id}.{dataset_id}.{table_name}")


if __name__ == "__main__":
    project_id = get_required_env("GCP_PROJECT_ID")
    dataset_id = get_required_env("DBT_DATASET_NAME")
    bucket_name = os.getenv("GCS_BUCKET_NAME") or get_required_env("BUCKET_NAME")
    bucket_prefix = os.getenv("GCS_BUCKET_PREFIX", "instacart_raw")
    table_names = ["aisles", "departments", "order_products__prior", "orders", "products"]
    create_table_bigquery_sql(table_names, dataset_id, project_id, bucket_name, bucket_prefix)
