pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "Mayur.Jadhav"
        LAMBDA_FUNCTION_NAME = "minimal_lambda"
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
            echo "Executing Terraform Validation"
            steps { sh "terraform validate" }
        }

        stage("Terraform Plan") {
            echo "Executing Terraform Plan"
            steps { sh "terraform plan -out=tfplan" }
        }

        stage("Terraform Apply") {
            echo "Executing Terraform Apply"
            steps { sh "terraform apply -auto-approve tfplan" }
        }

        stage("Invoke Lambda") {
            steps {
                echo "Executing Lambda Invoke"
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