pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "Mayur.Jadhav"
        LAMBDA_FUNCTION_NAME = "lambda_fun"
    }

//    stages {
//        stage("Checkout Code") {
//            steps {
//                git branch: 'main', url: 'https://github.com/maurjadhav/siemens_test.git'
//            }
//        }

        stage("Terraform Init") {
            steps {
                script {
                    echo "Initializing Terraform Backend"
                    sh """
                        terraform init \
                        -backend-config="bucket=$S3_BUCKET" \
                        -backend-config="key=$TF_STATE_KEY" \
                        -backend-config="region=$AWS_REGION"
                    """
                }
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
                script {
                    echo "Executing Terraform Plan"
                    sh "terraform plan"
                }
            }
        }

        stage("Terraform Apply") {
            steps {
                script {
                    echo "Applying Terraform Changes"
                    sh "terraform apply -auto-approve"
                }
            }
        }

        stage("Invoke Lambda") {
            steps {
                script {
                    echo "Invoking AWS Lambda Function"
                    sh """
                        aws lambda invoke \
                        --function-name $LAMBDA_FUNCTION_NAME \
                        --region $AWS_REGION \
                        --log-type Tail output.json
                    """
                }
            }
        }

        stage("Check CloudWatch Logs") {
            steps {
                script {
                    echo "Fetching CloudWatch Logs"
                    sh "aws logs tail /aws/lambda/$LAMBDA_FUNCTION_NAME --region $AWS_REGION --since 5m --format short"
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline execution failed!"
        }
    }
}
