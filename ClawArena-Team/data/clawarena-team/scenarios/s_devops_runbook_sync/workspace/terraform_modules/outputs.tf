# terraform_modules/outputs.tf

output "billing_db_param_group" {
  description = "RDS parameter group name for billing prod"
  value       = module.billing_rds_params.parameter_group_name
  # Expected value: pg-prod-billing-v3
}

output "payment_db_param_group" {
  description = "RDS parameter group name for payment prod"
  value       = module.payment_rds_params.parameter_group_name
}
