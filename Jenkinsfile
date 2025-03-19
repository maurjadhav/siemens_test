pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')          // Runs every 5 minutes
    }


    environment {
        AWS_REGION = "ap-south-1"
        S3_BUCKET  = "467.devops.candidate.exam"
        TF_STATE_KEY = "mayur jadhav"
        LAMBDA_FUNCTION_NAME = "invoke_api_lambda"
    }

    stages {
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
                    sh "terraform plan -out=tfplan"
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
