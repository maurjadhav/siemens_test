terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.91.0"
    }
  }

  backend "s3" {
    bucket = "467.devops.candidate.exam"
    region = "ap-south-1"
    key    = "Mayur.Jadhav"
  }
}

provider "aws" {
  region = "ap-south-1" # Don't change the region
}