terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "instacart-bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = false

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "instacart_warehouse" {
  dataset_id                 = var.bigquery_dataset_id
  friendly_name              = var.bigquery_dataset_friendly_name
  description                = var.bigquery_dataset_description
  location                   = var.bigquery_location
  delete_contents_on_destroy = false
}
