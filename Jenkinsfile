pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "Mayur.Jadhav"
        LAMBDA_FUNCTION_NAME = "new_mini_lambda_1"
    }

    stages {
        stage("Checkout Code") {
            steps {
                git branch: 'main', url: 'https://github.com/maurjadhav/siemens_test.git'
            }
        }

        stage("Package Lambda") {
            steps {
                echo "Packaging Lambda function"
                sh "zip lambda_function.zip lambda_function.py"
            }
        }

        stage("Terraform Init") {
            steps {
                sh """
                    terraform init \
                    -backend-config="bucket=$S3_BUCKET" \
                    -backend-config="key=$TF_STATE_KEY" \
                    -backend-config="region=$AWS_REGION"
                """
            }
        }

        stage("Terraform Validate") {
            steps { sh "terraform validate" }
        }

        stage("Terraform Plan") {
            steps { sh "terraform plan" }
        }

        stage("Terraform Apply") {
            steps { sh "terraform apply -auto-approve" }
        }

        stage("Invoke Lambda") {
            steps {
                sh """
                    aws lambda invoke \
                    --function-name $LAMBDA_FUNCTION_NAME \
                    --region $AWS_REGION \
                    --log-type Tail output.json
                """
            }
        }

        stage("Check CloudWatch Logs") {
            steps {
                sh "aws logs tail /aws/lambda/$LAMBDA_FUNCTION_NAME --region $AWS_REGION --since 5m --format short"
            }
        }
    }

    post {
        success { echo "Pipeline executed successfully!" }
        failure { echo "Pipeline execution failed!" }
    }
}