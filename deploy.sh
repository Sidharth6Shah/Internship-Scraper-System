#!/bin/bash
set -e

#AWS Lambda Deployment Script
#Configuration
AWS_REGION="us-east-1"
FUNCTION_NAME="internship-scraper"
ECR_REPO_NAME="internship-scraper"
IMAGE_TAG="latest"