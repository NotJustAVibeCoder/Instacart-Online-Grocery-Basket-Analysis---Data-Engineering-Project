terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project     = "instacart-basket-analysis"
  region      = "europe-west2"
}

resource "google_storage_bucket" "instacart-bucket" {
  name          = "instacart-bucket03211"
  location      = "europe-west2"
  force_destroy = true

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
  dataset_id                 = "instacart_warehouse0371"
  friendly_name              = "instacart-warehouse"
  description                = "Instacart analytics warehouse dataset"
  location                   = "europe-west2"
  delete_contents_on_destroy = true
}