# Terraform IaC for payments-split migration — billing service
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "payments-split-tfstate"
    prefix = "terraform/state/billing"
  }
}

variable "service_name" {
  default = "billing"
}

variable "project_id" {
  default = "payments-split-prod"
}

variable "region" {
  default = "us-central1"
}

locals {
  common_labels = {
    service     = "billing"
    environment = "production"
    managed_by  = "terraform"
    team        = "platform-migration"
  }
}

resource "google_cloud_run_service" "billing_service" {
  name     = "billing-service"
  location = var.region
  project  = var.project_id

  template {
    spec {
      service_account_name = "billing@${var.project_id}.iam.gserviceaccount.com"
      containers {
        image = "gcr.io/${var.project_id}/billing:latest"
        resources {
          limits = {
            cpu    = "2"
            memory = "512Mi"
          }
        }
        env {
          name = "SERVICE_NAME"
          value = "billing"
        }
        env {
          name = "ENV"
          value = "production"
        }
        env {
          name = "DB_SECRET"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.billing_db_secret.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
    metadata {
      labels = local.common_labels
      annotations = {
        "autoscaling.knative.dev/minScale" = "3"
        "autoscaling.knative.dev/maxScale" = "19"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_secret_manager_secret" "billing_db_secret" {
  secret_id = "billing-db-credentials"
  project   = var.project_id
  replication {
    automatic = true
  }
  labels = local.common_labels
}

resource "google_service_account" "billing_sa" {
  account_id   = "billing-service"
  display_name = "Billing Service Account (payments-split migration)"
  project      = var.project_id
}

resource "google_cloud_run_service_iam_member" "billing_invoker" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_service.billing_service.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.billing_sa.email}"
}

output "billing_url" {
  value = google_cloud_run_service.billing_service.status[0].url
}
