import kagglehub
import os

# # For local runs execute this in terminal:
# exprot DATA_DIR="data"
# uv run pipelines/download_datasets.py

# For Docker Airflow DATA_DIR is set in .env.airflow which is loaded during docker compose

dataset = "yasserh/instacart-online-grocery-basket-analysis-dataset"
base_data_dir = os.getenv("DATA_DIR", "data")
output_dir = os.path.join(base_data_dir, "instacart_raw")
force_download = os.getenv("FORCE_DOWNLOAD", "false").lower() == "true"

print("Download directory set to:", output_dir)
print("Force download set to:", force_download)

# Download latest version
def download_dataset(dataset: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    path = kagglehub.dataset_download(dataset, output_dir=output_dir, force_download=force_download)
    print("Download successful! Path to dataset files:", os.path.abspath(path))


if __name__ == "__main__":
    download_dataset(dataset, output_dir)