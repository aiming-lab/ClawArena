# terraform_modules/main.tf — Wave3 top-level module (source)
# The tfstate for this configuration is archived in tfstate_archive.tar.gz
# Run: tar -xzf tfstate_archive.tar.gz to extract terraform.tfstate

terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "mercatorrobotics-tfstate-prod"
    key    = "platform/billing/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

# Note: The billing RDS parameter group is "pg-prod-billing-v3"
# This value is confirmed in terraform.tfstate (extract from tfstate_archive.tar.gz)
module "billing_rds_params" {
  source             = "./rds_params"
  cluster_identifier = "billing-prod-cluster"
  log_min_duration_statement = 500
  lock_timeout       = 5000
}

module "payment_rds_params" {
  source             = "./rds_params"
  cluster_identifier = "payment-prod-cluster"
  log_min_duration_statement = 500
  lock_timeout       = 5000
}
