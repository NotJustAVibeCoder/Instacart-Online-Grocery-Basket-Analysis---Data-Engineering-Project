from __future__ import annotations

from datetime import datetime

import os

from airflow import DAG
from airflow.operators.bash import BashOperator


# This DAG runs the dataset download pipeline script.
# Note: the Airflow container must be able to access the repo's `pipelines/` and `data/` folders
# (e.g., via a volume mount or a custom Airflow image that includes the project code).

with DAG(
    dag_id="instacart_download_datasets",
    description="Download Instacart data and upload local data files to GCS",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["instacart", "kaggle", "data"],
) as dag:
    iac_dir = os.getenv("IAC_DIR", "/opt/airflow/iac")

    download_datasets = BashOperator(
        task_id="download_datasets",
        bash_command="python /opt/airflow/pipelines/download_datasets.py",
    )

    terraform_apply = BashOperator(
        task_id="create_gcs_infrastructure",
        bash_command=(
            f"cd {iac_dir} && "
            "terraform init && "
            "terraform apply -auto-approve"
        ),
    )

    upload_data_to_gcs = BashOperator(
        task_id="upload_data_to_gcs",
        bash_command="python /opt/airflow/pipelines/upload_data_to_gcs.py",
    )

    create_external_tables = BashOperator(
        task_id="BigQuery_create_external_tables",
        bash_command="python /opt/airflow/pipelines/create_external_tables.py",
    )

    download_datasets >> terraform_apply >> upload_data_to_gcs >> create_external_tables

