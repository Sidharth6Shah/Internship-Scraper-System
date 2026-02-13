#!/bin/bash
set -e

#AWS Lambda Deployment Script
#Configuration
AWS_REGION="us-east-1"
FUNCTION_NAME="internship-scraper"
ECR_REPO_NAME="internship-scraper"
IMAGE_TAG="latest"

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ -z "$AWS_ACCOUNT_ID" ]; then
    exit 1
fi

#Package the code into a container
docker build -t ${FUNCTION_NAME}:${IMAGE_TAG} .

#Log into ECR
aws ecr get-login-password --region ${AWS_REGION} | \
docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

#Create/clear space in ecr
aws ecr describe-repositories --repository-names ${ECR_REPO_NAME} --region ${AWS_REGION} > /dev/null 2>&1
if [ $? -ne 0 ]; then
    aws ecr create-repository --repository-name ${ECR_REPO_NAME} --region ${AWS_REGION}
else
    # aws ecr batch-delete-image --repository-name ${ECR_REPO_NAME} --image-ids $(aws ecr list-images --repository-name ${ECR_REPO_NAME} --query 'imageIds[*]' --output json) --region ${AWS_REGION}
fi

#Label package
ECR_IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}"
docker tag ${FUNCTION_NAME}:${IMAGE_TAG} ${ECR_IMAGE_URI}

#Push to ecr
docker push ${ECR_IMAGE_URI}

#Update Lambda function
aws lambda update-function-code \
    --function-name ${FUNCTION_NAME} \
    --image-uri ${ECR_IMAGE_URI} \
    --region ${AWS_REGION} > /dev/null
if [ $? -ne 0 ]; then
    exit 1
fi

aws lambda wait function-updated --function-name ${FUNCTION_NAME} --region ${AWS_REGION}