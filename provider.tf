terraform {
  required_version = ">= 1.0.0"

  backend "s3" { # Terraform backend configuration
    bucket = "467.devops.candidate.exam"
    key    = "mayur.jadhav"
    region = "ap-south-1"
  }
}

provider "aws" {
  region = "ap-south-1" # Don't change the region
}