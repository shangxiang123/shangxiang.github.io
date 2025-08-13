# Terraform (AWS) — Overview

This folder contains Terraform modules and environment definitions to provision AWS resources for AIS Chatrooms.

Planned resources (dev):
- VPC (2 AZ), subnets, NAT/IGW, security groups
- RDS PostgreSQL
- ElastiCache Redis (optional for workers)
- ECR repositories (api, web)
- ECS (Fargate) cluster and services (api, web) with ALB + ACM cert
- S3 (static assets, logs), CloudFront (optional)
- IAM roles for tasks, SSM/Secrets Manager for secrets

Usage (example):
```
cd infra/terraform/envs/dev
terraform init
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```

Note: Backend state recommended (S3 + DynamoDB lock). Fill in provider credentials via AWS_PROFILE or env vars.