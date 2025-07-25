terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configure the AWS Provider (if you need authentication)
# provider "aws" {
#  region = "eu-north-1"
#  access_key = var.aws_access_key_id
#  secret_key = var.aws_secret_access_key
#}

# S3 Bucket for artifacts
resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket = "mlflow-artifacts-bucket-m5"
  force_destroy = true
}


