# terraform_modules/variables.tf

variable "environment" {
  description = "Deployment environment (prod / staging / dev)"
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "Primary AWS region"
  type        = string
  default     = "us-east-1"
}

variable "billing_db_param_group_name" {
  description = "RDS parameter group name for billing prod DB"
  type        = string
  default     = "pg-prod-billing-v3"
}

variable "lock_timeout_ms" {
  description = "DDL lock timeout in milliseconds (post-incident: 5000 = 5s)"
  type        = number
  default     = 5000
}
