terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
  # backend "s3" {
  #   bucket = "your-tf-state-bucket"
  #   key    = "ais-chatrooms/dev/terraform.tfstate"
  #   region = "ap-southeast-1"
  #   dynamodb_table = "your-tf-locks"
  # }
}

provider "aws" {
  region = var.region
}

variable "region" { type = string default = "ap-southeast-1" }

# TODO: call modules for network, rds, ecr, ecs, alb, etc.

output "region" { value = var.region }