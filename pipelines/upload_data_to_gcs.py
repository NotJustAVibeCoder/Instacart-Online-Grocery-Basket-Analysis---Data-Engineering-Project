from __future__ import annotations

import os
from pathlib import Path

from google.cloud import storage


def upload_directory_to_bucket(local_dir: Path, bucket_name: str, prefix: str = "") -> None:
    if not local_dir.exists():
        raise SystemExit(f"Local directory does not exist: {local_dir}")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    files = [p for p in local_dir.rglob("*") if p.is_file()]
    if not files:
        print(f"No files found in {local_dir}. Nothing to upload.")
        return

    for file_path in files:
        rel_path = file_path.relative_to(local_dir).as_posix()
        blob_name = f"{prefix.rstrip('/')}/{rel_path}" if prefix else rel_path
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(file_path))
        print(f"Uploaded {file_path} -> gs://{bucket_name}/{blob_name}")


def main() -> None:
    data_dir = Path(os.getenv("DATA_DIR", "/opt/airflow/data")).resolve()
    bucket_name = os.getenv("GCS_BUCKET_NAME") or os.getenv("BUCKET_NAME", "instacart-bucket03211")
    bucket_prefix = os.getenv("GCS_BUCKET_PREFIX", "")

    print(f"Uploading files from: {data_dir}")
    print(f"Destination bucket: gs://{bucket_name}/{bucket_prefix}")

    upload_directory_to_bucket(data_dir, bucket_name, bucket_prefix)


if __name__ == "__main__":
    main()

