# Instacart-Online-Grocery-Basket-Analysis---Data-Engineering-Project
This project is the capstone submission for the DataTalksClub Data Engineering Zoomcamp. The goal is to apply everything learned in the course to build a fully reproducible, end-to-end ELT data pipeline using the Instacart Online Grocery Basket Analysis dataset from Kaggle. 

## Reproduction Steps

### 1) Clone repository

```bash
git clone https://github.com/<your-org-or-username>/Instacart-Online-Grocery-Basket-Analysis---Data-Engineering-Project.git
cd Instacart-Online-Grocery-Basket-Analysis---Data-Engineering-Project
```

### 2) Configure Terraform variables

The Terraform configuration lives in `iac/` and uses `variables.tf` for input definitions.
Copy the example values file and replace the placeholders with your own GCP values:

```bash
cp iac/terraform.tfvars.example iac/terraform.tfvars
```

The example file includes:

```hcl
project_id                     = "your-gcp-project-id"
region                         = "europe-west2"
bucket_name                    = "your-unique-gcs-bucket-name"
bigquery_dataset_id            = "instacart_warehouse_dev"
bigquery_dataset_friendly_name = "instacart-warehouse"
bigquery_dataset_description   = "Instacart analytics warehouse dataset"
bigquery_location              = "europe-west2"
```

`iac/terraform.tfvars` is ignored by Git, so you can keep your real project-specific values there safely.

### 3) Configure local environment variables

This project uses `direnv` so project variables are loaded into your shell automatically when you enter the repository.

1. Install `direnv` and hook it into your shell.
2. Copy the example file:

```bash
cp .env.example .env
```

3. Fill in your real values in `.env`.
4. Approve the repo once:

```bash
direnv allow
```

After that, each new shell session in this project will automatically load the values from `.env`.

Local defaults provided by `.envrc`:
- `DATA_DIR` -> `<repo>/data`
- `IAC_DIR` -> `<repo>/iac`
- `DBT_PROFILES_DIR` -> `<repo>/analytics`
- `AIRFLOW_UID` -> your local user id

If you need machine-specific overrides, create `.env.local`. It is also loaded automatically and is ignored by Git.

### 4) Provision infrastructure with Terraform

Run Terraform from the `iac/` directory:

```bash
terraform -chdir=iac init
terraform -chdir=iac plan
terraform -chdir=iac apply
```

This provisions:
- a Google Cloud Storage bucket for raw Instacart data
- a BigQuery dataset for the warehouse

You can inspect the provisioned values with:

```bash
terraform -chdir=iac output
```

### 5) Configure Airflow environment variables

Copy the example Airflow env file:

```bash
cp .env.airflow.example .env.airflow
```

Then update it with your container-specific values:

```env
DATA_DIR=/opt/airflow/data
KAGGLE_USERNAME=<your_kaggle_username>
KAGGLE_KEY=<your_kaggle_api_key>
```

Notes:
- `DATA_DIR` points to the mounted folder inside the Airflow container.
- `KAGGLE_USERNAME` and `KAGGLE_KEY` are required by `kagglehub` in `pipelines/download_datasets.py`.
- `.env.airflow` is for Docker Compose containers. `.env` is for your local shell session.

### 6) Build and start Airflow with Docker Compose

```bash
docker compose up --build -d
```

Airflow UI will be available at [http://localhost:8080](http://localhost:8080).

### 7) Run the DAG

1. Open Airflow UI.
2. Find DAG: `instacart_download_datasets`.
3. Enable the DAG toggle.
4. Click **Trigger DAG**.

This runs `dags/instacart_dag.py`, which executes:

`python /opt/airflow/pipelines/download_datasets.py`

### 8) Verify downloaded data

After the DAG run succeeds, dataset files should be present in your local `data/` folder (mounted to `/opt/airflow/data` in the container).
