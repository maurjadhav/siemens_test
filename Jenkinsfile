pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "mayur.jadhav"
        LAMBDA_FUNCTION_NAME = "qwerty_123"
    }

    stages {
        stage("Package Lambda") {
            steps {
                echo "Packaging Lambda function"
                sh "zip lambda_function45.zip lambda_function.py"
            }
        }

        stage("Terraform Init") {
            steps {
                echo "Executing Terraform Init"
                sh "terraform init"
            }
        }

        stage("Terraform Validate") {
            steps {
                script {
                    echo "Validating Terraform Code"
                    sh "terraform validate"
                }
            }
        }

        stage("Terraform Plan") {
            steps {
                echo "Executing Terraform Plan"
                sh "terraform plan"
            }
        }

        stage("Terraform Apply") {
            steps {
                echo "Executing Terraform Apply"
                sh "terraform apply -auto-approve"
            }
        }

        stage("Invoke Lambda") {
            steps {
                echo "Invoking AWS Lambda Function"
                sh """
                    aws lambda invoke --function-name $LAMBDA_FUNCTION_NAME --log-type Tail output.json
                    jq -r '.LogResult' output.json | base64 --decode
                """
            }
        }
    }
}
