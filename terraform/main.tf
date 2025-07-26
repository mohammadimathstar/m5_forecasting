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

# S3 Bucket for processed data
resource "aws_s3_bucket" "m5_data" {
  bucket        = "data-bucket-m5"
  force_destroy = true
}

# S3 Bucket for artifacts
resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket        = "mlflow-artifacts-bucket-m5"
  force_destroy = true
}

# S3 Bucket for dev_codes
resource "aws_s3_bucket" "m5_dev_codes" {
  bucket        = "development-codes-bucket-m5"
  force_destroy = true
}

# S3 Bucket for codes
# resource "aws_s3_bucket" "m5_prod_codes" {
#  bucket        = "production-codes-bucket-m5"
#  force_destroy = true
#}

