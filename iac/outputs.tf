output "bucket_name" {
  description = "Provisioned GCS bucket for raw Instacart data."
  value       = google_storage_bucket.instacart-bucket.name
}

output "bigquery_dataset_id" {
  description = "Provisioned BigQuery dataset ID."
  value       = google_bigquery_dataset.instacart_warehouse.dataset_id
}

output "bigquery_dataset_self_link" {
  description = "BigQuery dataset self link."
  value       = google_bigquery_dataset.instacart_warehouse.self_link
}
