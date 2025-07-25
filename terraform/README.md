# 🛠️ Terraform Infrastructure for Model Artifact Storage

This directory contains Terraform configuration used to provision cloud infrastructure resources needed for the project.

## 🎯 Purpose

The primary goal of this Terraform module is to:

- Provision an **Amazon S3 bucket** to store ML model artifacts (e.g., models logged via MLflow).
- Configure the bucket with appropriate policies for versioning and access.

This infrastructure enables persistent and centralized storage of trained models for future use, deployment, and auditing.

## 🧱 Resource Overview

| Resource Type | Description                     |
|---------------|---------------------------------|
| `aws_s3_bucket` | Bucket to store MLflow artifacts |
| `aws_s3_bucket_versioning` | Enables versioning for artifact tracking |
| `aws_s3_bucket_policy` | Optional: Configure read/write permissions |

## 🧩 Prerequisites

Before using this Terraform setup, ensure the following:

- [Terraform](https://www.terraform.io/downloads.html) is installed (version ≥ 1.0).
- AWS credentials are configured on your system via one of the following:
  - `~/.aws/credentials`
  - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
  - IAM Role (if running on EC2 or similar)

## 🚀 How to Use

1. Navigate to the terraform directory:

   ```bash
   cd terraform
   ```
   

2. Initialize the Terraform working directory:

```bash
terraform init
```

3. Review the plan before applying:

```bash
terraform plan
```

4. Apply the configuration to create the resources:

```bash
terraform apply
```

Confirm when prompted with `yes`.

### 🧹 Teardown (Optional)

If you want to destroy the created resources:

```bash
terraform destroy
```

## 📁 Output

After successful deployment, you should see the S3 bucket name in the output. You can now update your MLflow tracking configuration to use this bucket as the --default-artifact-root.

## 📝 Notes

- Make sure your .env or MLflow configuration uses the same bucket name and region.
