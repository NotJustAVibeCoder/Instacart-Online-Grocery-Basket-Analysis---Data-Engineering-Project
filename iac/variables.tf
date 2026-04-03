variable "project_id" {
  description = "GCP project ID used for Instacart infrastructure."
  type        = string
  default     = "instacart-basket-analysis"
}

variable "region" {
  description = "Primary GCP region for regional resources."
  type        = string
  default     = "europe-west2"
}

variable "bucket_name" {
  description = "Name of the GCS bucket used for raw Instacart files."
  type        = string
  default     = "instacart-bucket03211"
}

variable "bigquery_dataset_id" {
  description = "BigQuery dataset ID for the warehouse dataset."
  type        = string
  default     = "instacart_warehouse0371"
}

variable "bigquery_dataset_friendly_name" {
  description = "Human-readable name for the BigQuery dataset."
  type        = string
  default     = "instacart-warehouse"
}

variable "bigquery_dataset_description" {
  description = "Description for the BigQuery dataset."
  type        = string
  default     = "Instacart analytics warehouse dataset"
}

variable "bigquery_location" {
  description = "BigQuery location for the dataset."
  type        = string
  default     = "europe-west2"
}
