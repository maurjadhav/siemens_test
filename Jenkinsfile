pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "mayur.jadhav"
        LAMBDA_FUNCTION_NAME = "invoke_api_lambda"
    }

    stages {
        stage("Package Lambda") {
            steps {
                sh "zip lambda_function.zip lambda_function.py"
            }
        }

        stage("Terraform Init") {
            steps {
                sh "terraform init"
            }
        }

        stage("Terraform Plan") {
            steps {
                sh "terraform plan"
            }
        }

        stage("Terraform Apply") {
            steps {
                sh "terraform apply -auto-approve"
            }
        }

        stage("Invoke Lambda") {
            steps {
                sh """
                    aws lambda invoke --function-name $LAMBDA_FUNCTION_NAME --log-type Tail output.json
                    jq -r '.LogResult' output.json | base64 --decode
                """
            }
        }
    }
}
