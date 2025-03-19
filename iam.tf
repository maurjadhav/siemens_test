resource "aws_iam_policy" "lambda_tag_policy" {
  name        = "LambdaTagPolicy"
  description = "Policy to allow tagging Lambda functions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["lambda:CreateFunction", "lambda:TagResource"]
        Resource = "arn:aws:lambda:ap-south-1:168009530589:function:invoke_api_lambda"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_lambda_tag_policy" {
  policy_arn = aws_iam_policy.lambda_tag_policy.arn
  role       = "jenkins-role"
}
