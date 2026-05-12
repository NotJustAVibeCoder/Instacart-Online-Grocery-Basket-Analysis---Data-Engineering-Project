# Instacart rpt Dashboard

Interactive Streamlit dashboard for the dbt reporting tables:

- `rpt_department_summary`
- `rpt_aisle_summary`
- `rpt_user_order_summary`

## Run locally

Set the same BigQuery environment variables used by dbt:

```bash
export GCP_PROJECT_ID=your-gcp-project-id
export DBT_DATASET_NAME=instacart_warehouse_dev
export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/credentials/service-account.json
```

Then start the dashboard:

```bash
uv run streamlit run dashboard/app.py
```

The dashboard reads the rpt tables directly from BigQuery and keeps results cached for 15 minutes.
