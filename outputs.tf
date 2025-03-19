output "subnet_id" {
  value = aws_subnet.private_subnet.id
}

output "lambda_function" {
  value = aws_lambda_function.lambda_function.function_name
}
