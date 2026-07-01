# Terraform IaC for payments-split migration — payments service
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "payments-split-tfstate"
    prefix = "terraform/state/payments"
  }
}

variable "service_name" {
  default = "payments"
}

variable "project_id" {
  default = "payments-split-prod"
}

variable "region" {
  default = "us-central1"
}

locals {
  common_labels = {
    service     = "payments"
    environment = "production"
    managed_by  = "terraform"
    team        = "platform-migration"
  }
}

resource "google_cloud_run_service" "payments_service" {
  name     = "payments-service"
  location = var.region
  project  = var.project_id

  template {
    spec {
      service_account_name = "payments@${var.project_id}.iam.gserviceaccount.com"
      containers {
        image = "gcr.io/${var.project_id}/payments:latest"
        resources {
          limits = {
            cpu    = "1"
            memory = "2048Mi"
          }
        }
        env {
          name = "SERVICE_NAME"
          value = "payments"
        }
        env {
          name = "ENV"
          value = "production"
        }
        env {
          name = "DB_SECRET"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.payments_db_secret.secret_id
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
        "autoscaling.knative.dev/maxScale" = "12"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_secret_manager_secret" "payments_db_secret" {
  secret_id = "payments-db-credentials"
  project   = var.project_id
  replication {
    automatic = true
  }
  labels = local.common_labels
}

resource "google_service_account" "payments_sa" {
  account_id   = "payments-service"
  display_name = "Payments Service Account (payments-split migration)"
  project      = var.project_id
}

resource "google_cloud_run_service_iam_member" "payments_invoker" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_service.payments_service.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.payments_sa.email}"
}

output "payments_url" {
  value = google_cloud_run_service.payments_service.status[0].url
}
