# Terraform IaC for payments-split migration — ledger service
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "payments-split-tfstate"
    prefix = "terraform/state/ledger"
  }
}

variable "service_name" {
  default = "ledger"
}

variable "project_id" {
  default = "payments-split-prod"
}

variable "region" {
  default = "us-central1"
}

locals {
  common_labels = {
    service     = "ledger"
    environment = "production"
    managed_by  = "terraform"
    team        = "platform-migration"
  }
}

resource "google_cloud_run_service" "ledger_service" {
  name     = "ledger-service"
  location = var.region
  project  = var.project_id

  template {
    spec {
      service_account_name = "ledger@${var.project_id}.iam.gserviceaccount.com"
      containers {
        image = "gcr.io/${var.project_id}/ledger:latest"
        resources {
          limits = {
            cpu    = "3"
            memory = "2048Mi"
          }
        }
        env {
          name = "SERVICE_NAME"
          value = "ledger"
        }
        env {
          name = "ENV"
          value = "production"
        }
        env {
          name = "DB_SECRET"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.ledger_db_secret.secret_id
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
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_secret_manager_secret" "ledger_db_secret" {
  secret_id = "ledger-db-credentials"
  project   = var.project_id
  replication {
    automatic = true
  }
  labels = local.common_labels
}

resource "google_service_account" "ledger_sa" {
  account_id   = "ledger-service"
  display_name = "Ledger Service Account (payments-split migration)"
  project      = var.project_id
}

resource "google_cloud_run_service_iam_member" "ledger_invoker" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_service.ledger_service.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.ledger_sa.email}"
}

output "ledger_url" {
  value = google_cloud_run_service.ledger_service.status[0].url
}
