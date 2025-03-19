pipeline {
    agent any

//    triggers {
//        pollSCM('H/5 * * * *')  // Uncomment to run every 5 minutes
//    }

    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "mayur jadhav"
        LAMBDA_FUNCTION_NAME = "invoke_api_lambda"
    }

    stages {
        stage("Package Lambda Function") {
            steps {
                script {
                    echo "Packaging Lambda function"
                    sh """
                        zip lambda_function.zip lambda_function.py || echo "Lambda function packaging failed!"
                    """
                }
            }
        }

        stage("TF Init") {
            steps {
                script {
                    echo "Executing Terraform Init"
                    sh """
                        terraform init \
                        -backend-config="bucket=$S3_BUCKET" \
                        -backend-config="key=$TF_STATE_KEY" \
                        -backend-config="region=$AWS_REGION"
                    """
                }
            }
        }

        stage("TF Validate") {
            steps {
                script {
                    echo "Validating Terraform Code"
                    sh "terraform validate"
                }
            }
        }

        stage("TF Plan") {
            steps {
                script {
                    echo "Executing Terraform Plan"
                    sh "terraform plan"
                }
            }
        }

        stage("TF Apply") {
            steps {
                script {
                    echo "Executing Terraform Apply"
                    sh "terraform apply -auto-approve"
                }
            }
        }

//        stage("Invoke Lambda") {
//            steps {
//                script {
//                    echo "Invoking AWS Lambda Function"
//                    sh """
//                        aws lambda invoke \
//                        --function-name $LAMBDA_FUNCTION_NAME \
//                        --region $AWS_REGION \
//                        --log-type Tail \
//                        output.json > lambda_response.json
//
//                        # Extract and decode the LogResult
//                        LOG_RESULT=\$(jq -r '.LogResult' lambda_response.json)
//                        echo \$LOG_RESULT | base64 --decode
//                    """
//                }
//            }
//        }

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
