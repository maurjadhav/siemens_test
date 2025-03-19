# IAM policy for Jenkins role
resource "aws_iam_policy" "jenkins_policy" {
  name = "jenkins-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:DisassociateRouteTable",
          "ec2:AssociateRouteTable",
          "ec2:CreateRouteTable",
          "ec2:DeleteRouteTable",
          "ec2:CreateSubnet",
          "ec2:DeleteSubnet",
          "ec2:CreateSecurityGroup",
          "ec2:DeleteSecurityGroup",
          "ec2:AuthorizeSecurityGroupEgress",
          "ec2:RevokeSecurityGroupEgress",
          "ec2:CreateTags",
          "ec2:DeleteTags",
          "ec2:DescribeVpcs",
          "ec2:DescribeSubnets",
          "ec2:DescribeRouteTables",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeAvailabilityZones",
          "ec2:DescribeNatGateways",
          "lambda:CreateFunction",
          "lambda:DeleteFunction",
          "lambda:UpdateFunctionCode",
          "lambda:UpdateFunctionConfiguration",
          "lambda:InvokeFunction",
          "lambda:GetFunction",
          "lambda:ListFunctions",
          "logs:CreateLogGroup",
          "logs:DeleteLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams",
          "logs:GetLogEvents",
          "logs:FilterLogEvents",
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach the policy to the Jenkins role
resource "aws_iam_role_policy_attachment" "jenkins_policy_attachment" {
  role       = "jenkins-role"  # Replace with your actual Jenkins role name
  policy_arn = aws_iam_policy.jenkins_policy.arn
} 