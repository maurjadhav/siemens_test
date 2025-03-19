# Private Subnet inside existing VPC
resource "aws_subnet" "private_subnet" {
  vpc_id                  = data.aws_vpc.vpc.id
  cidr_block              = "10.0.4.0/24"            # Choose any available subnet CIDR
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = false

  tags = {
    Name = "Private-Subnet"
  }
}

# Route Table & Association with Private Subnet
resource "aws_route_table" "private_rt" {
  vpc_id = data.aws_vpc.vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = data.aws_nat_gateway.nat.id
  }

  tags = {
    Name = "Private-RT"
  }
}

# Associate Route Table with Private Subnet
resource "aws_route_table_association" "private_assoc" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_rt.id

  depends_on = [aws_subnet.private_subnet]                # Ensures the subnet is created first
}

# Security Group for Lambda inside VPC
resource "aws_security_group" "lambda_sg" {
  name_prefix = "lambda-sg"
  vpc_id      = data.aws_vpc.vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Lambda-SG"
  }
}

# AWS Lambda Function inside the VPC
resource "aws_lambda_function" "lambda_function" {
  function_name = "mini"
  role          = data.aws_iam_role.lambda.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  filename      = "lambda_function.zip"
  timeout       = 60

  environment {
    variables = {
      SUBNET_ID = aws_subnet.private_subnet.id
      NAME      = "Mayur Jadhav"
      EMAIL     = "mr.jadhav1205@gmail.com"
    }
  }

  vpc_config {
    subnet_ids         = [aws_subnet.private_subnet.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"
  retention_in_days = 7

  depends_on = [aws_lambda_function.lambda_function] # Ensure Lambda exists first
}