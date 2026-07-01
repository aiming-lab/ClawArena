# terraform_modules/ — Terraform IaC modules

## Files

| File | Description |
|---|---|
| tfstate_archive.tar.gz | **B-dimension**: Compressed tfstate — must `tar -xzf` to read. Contains `terraform.tfstate` with RDS parameter group names. |
| main.tf | Top-level Terraform module source |
| variables.tf | Variable definitions |
| outputs.tf | Output values (billing param group = pg-prod-billing-v3) |
| rds_params/ | aws_db_parameter_group module |

**Note**: `terraform.tfstate` is only accessible after extracting the tar.gz archive:
```bash
tar -xzf tfstate_archive.tar.gz
```
