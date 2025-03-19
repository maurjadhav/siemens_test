# Fetch existing VPC
data "aws_vpc" "vpc" {
  id = "vpc-06b326e20d7db55f9"
}

# Fetch existing NAT Gateway
data "aws_nat_gateway" "nat" {
  id = "nat-0a34a8efd5e420945"
}

# Fetch existing IAM Role for Lambda
data "aws_iam_role" "lambda" {
  name = "DevOps-Candidate-Lambda-Role"
}
