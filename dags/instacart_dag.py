from __future__ import annotations

from datetime import datetime

import os
import shlex

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


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
    dbt_project_dir = os.getenv("DBT_PROJECT_DIR", "/opt/airflow/analytics")
    dbt_profiles_dir = os.getenv("DBT_PROFILES_DIR", dbt_project_dir)

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

    run_dbt_models = BashOperator(
        task_id="BigQuery_run_dbt_models",
        bash_command=(
            "set -euo pipefail\n"
            'export PATH="/opt/airflow/.venv/bin:${PATH}"\n'
            'test -f "${GOOGLE_APPLICATION_CREDENTIALS:?GOOGLE_APPLICATION_CREDENTIALS must be set}"\n'
            "command -v dbt\n"
            "dbt run "
            f"--project-dir {shlex.quote(dbt_project_dir)} "
            f"--profiles-dir {shlex.quote(dbt_profiles_dir)} "
            "--target dev"
        ),
        append_env=True,
    )

    download_datasets >> terraform_apply >> upload_data_to_gcs >> create_external_tables >> run_dbt_models
