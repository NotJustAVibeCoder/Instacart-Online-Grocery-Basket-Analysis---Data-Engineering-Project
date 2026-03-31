from __future__ import annotations

from google.cloud import bigquery


CREATE_AISLES_EXTERNAL_SQL = """
CREATE OR REPLACE EXTERNAL TABLE `instacart-basket-analysis.instacart_warehouse0371.aisles_external`
OPTIONS (
  format = 'CSV',
  uris = [
    'gs://instacart-bucket03211/instacart_raw/aisles.csv'
  ]
);
"""


def main() -> None:
    client = bigquery.Client(project="instacart-basket-analysis")
    job = client.query(CREATE_AISLES_EXTERNAL_SQL)
    job.result()
    print("Created/updated external table: instacart_warehouse0371.aisles_external")


if __name__ == "__main__":
    main()

