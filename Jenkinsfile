pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "Mayur.Jadhav"
        LAMBDA_FUNCTION_NAME = "abc"
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
                    echo "Executing Terraform Apply"
                    sh "terraform apply -auto-approve"
                }
            }
        }

        stage("Invoke Lambda") {
            steps {
                script {
                    try {
                        echo "Invoking AWS Lambda Function: ${LAMBDA_FUNCTION_NAME}"
                        def response = sh(script: """
                            aws lambda invoke \
                            --function-name ${LAMBDA_FUNCTION_NAME} \
                            --region ${AWS_REGION} \
                            --payload '{"subnet_id": "test-subnet"}' \
                            --log-type Tail \
                            --cli-binary-format raw-in-base64-out \
                            output.json
                        """, returnStdout: true).trim()
                        
                        // Read and display the response
                        def output = readFile('output.json')
                        echo "Lambda response: ${output}"
                        
                        // Check if the invocation was successful
                        if (response.contains("StatusCode")) {
                            echo "Lambda function invoked successfully!"
                        } else {
                            error "Lambda invocation failed: ${response}"
                        }
                    } catch (Exception e) {
                        error "Lambda invocation failed: ${e.getMessage()}"
                    }
                }
            }
        }

        stage("Check CloudWatch Logs") {
            steps {
                script {
                    echo "Fetching AWS Lambda Logs from CloudWatch"
                    sh """
                        aws logs tail /aws/lambda/$LAMBDA_FUNCTION_NAME \
                        --region $AWS_REGION \
                        --since 5m \
                        --format short
                    """
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
