# Terraform IaC for payments-split migration — reports service
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "payments-split-tfstate"
    prefix = "terraform/state/reports"
  }
}

variable "service_name" {
  default = "reports"
}

variable "project_id" {
  default = "payments-split-prod"
}

variable "region" {
  default = "us-central1"
}

locals {
  common_labels = {
    service     = "reports"
    environment = "production"
    managed_by  = "terraform"
    team        = "platform-migration"
  }
}

resource "google_cloud_run_service" "reports_service" {
  name     = "reports-service"
  location = var.region
  project  = var.project_id

  template {
    spec {
      service_account_name = "reports@${var.project_id}.iam.gserviceaccount.com"
      containers {
        image = "gcr.io/${var.project_id}/reports:latest"
        resources {
          limits = {
            cpu    = "2"
            memory = "512Mi"
          }
        }
        env {
          name = "SERVICE_NAME"
          value = "reports"
        }
        env {
          name = "ENV"
          value = "production"
        }
        env {
          name = "DB_SECRET"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.reports_db_secret.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
    metadata {
      labels = local.common_labels
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "5"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_secret_manager_secret" "reports_db_secret" {
  secret_id = "reports-db-credentials"
  project   = var.project_id
  replication {
    automatic = true
  }
  labels = local.common_labels
}

resource "google_service_account" "reports_sa" {
  account_id   = "reports-service"
  display_name = "Reports Service Account (payments-split migration)"
  project      = var.project_id
}

resource "google_cloud_run_service_iam_member" "reports_invoker" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_service.reports_service.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.reports_sa.email}"
}

output "reports_url" {
  value = google_cloud_run_service.reports_service.status[0].url
}
