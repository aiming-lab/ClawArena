# infra/tf/main.tf — Terraform: checkout-service Redis ElastiCache provisioning.
#
# NOTE: The redis_connection_pool_size variable was erroneously set to 5
#       in the 2026-05-20 "cost-optimisation" PR. Should be 20.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "redis_connection_pool_size" {
  description = "Redis connection pool size per checkout-service instance"
  type        = number
  default     = 5  # v3.2.1 regression — was 20 in v3.1.x
}

variable "checkout_instance_count" {
  description = "Number of checkout-service replicas"
  type        = number
  default     = 8
}

resource "aws_elasticache_cluster" "checkout_redis" {
  cluster_id           = "checkout-redis-prod"
  engine               = "redis"
  node_type            = "cache.r7g.large"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379

  tags = {
    Service = "checkout-service"
    Env     = "production"
    Pool    = "max_${var.redis_connection_pool_size}"
  }
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.checkout_redis.cache_nodes[0].address
}

output "effective_pool_size" {
  value = var.redis_connection_pool_size
}
