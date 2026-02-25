# AWS Lambda Deployment Guide

Complete guide for deploying the internship scraper to AWS Lambda.

---

## Prerequisites

Before deploying, ensure you have:

- **AWS Account** with billing enabled
- **AWS CLI** installed and configured (`aws configure`)
- **Docker** installed and running
- **Git** for version control

---

## One-Time AWS Setup

### 1. Create DynamoDB Table

**Via AWS Console:**
1. Go to DynamoDB → Tables → Create table
2. Table name: `internships-jobs` (or your choice)
3. Partition key: `job_id` (String)
4. Leave other settings as default
5. Create table

**Via AWS CLI:**
```bash
aws dynamodb create-table \
    --table-name internships-jobs \
    --attribute-definitions AttributeName=job_id,AttributeType=S \
    --key-schema AttributeName=job_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

---

### 2. Create Lambda IAM Role

This role allows Lambda to access DynamoDB and write logs.

```bash
# Create role
aws iam create-role \
    --role-name lambda-scraper-role \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "lambda.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }]
    }'

# Attach basic Lambda execution policy (for CloudWatch logs)
aws iam attach-role-policy \
    --role-name lambda-scraper-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Attach DynamoDB full access
aws iam attach-role-policy \
    --role-name lambda-scraper-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
```

---

### 3. Create Lambda Function (First Time)

**Important:** Run `./deploy.sh` first to build and push the Docker image to ECR.

Then create the Lambda function:

```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="us-east-1"

aws lambda create-function \
    --function-name internship-scraper \
    --package-type Image \
    --code ImageUri=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/internship-scraper:latest \
    --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/lambda-scraper-role \
    --timeout 900 \
    --memory-size 2048 \
    --region ${AWS_REGION}
```

**Configuration:**
- `timeout`: 900 seconds (15 minutes max)
- `memory-size`: 2048 MB (Chromium needs memory)

---

### 4. Set Environment Variables

Lambda needs to know your DynamoDB table name and Discord webhook:

```bash
aws lambda update-function-configuration \
    --function-name internship-scraper \
    --environment "Variables={
        DYNAMODB_TABLE_NAME=internships-jobs,
        DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL
    }" \
    --region us-east-1
```

---

### 5. Create EventBridge Schedule

Schedule Lambda to run daily at 9 AM UTC.

**Via AWS Console:**
1. Go to EventBridge → Rules → Create rule
2. Name: `daily-scraper-schedule`
3. Rule type: Schedule
4. Schedule pattern: Cron expression
5. Cron: `0 9 * * ? *` (9 AM UTC daily)
6. Target: Lambda function `internship-scraper`
7. Create rule

**Via AWS CLI:**
```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="us-east-1"

# Create EventBridge rule
aws events put-rule \
    --name daily-scraper-schedule \
    --schedule-expression "cron(0 9 * * ? *)" \
    --region ${AWS_REGION}

# Grant EventBridge permission to invoke Lambda
aws lambda add-permission \
    --function-name internship-scraper \
    --statement-id eventbridge-invoke \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:${AWS_REGION}:${AWS_ACCOUNT_ID}:rule/daily-scraper-schedule \
    --region ${AWS_REGION}

# Set Lambda as target
aws events put-targets \
    --rule daily-scraper-schedule \
    --targets "Id=1,Arn=arn:aws:lambda:${AWS_REGION}:${AWS_ACCOUNT_ID}:function:internship-scraper" \
    --region ${AWS_REGION}
```

---

## Deploying Code Updates

After making changes to your code:

```bash
# Make deploy script executable (first time only)
chmod +x deploy.sh

# Deploy
./deploy.sh
```

This will:
1. Build Docker image (~5 minutes)
2. Push to ECR (~5 minutes)
3. Update Lambda function (~1 minute)

---

## Testing the Function

### Manual Invocation

Test Lambda manually:

```bash
aws lambda invoke \
    --function-name internship-scraper \
    --region us-east-1 \
    response.json

# View output
cat response.json
```

---

## Monitoring

### View Lambda Logs

**Via AWS Console:**
1. Go to CloudWatch → Log groups
2. Find `/aws/lambda/internship-scraper`
3. View log streams

**Via AWS CLI:**
```bash
# Tail logs in real-time
aws logs tail /aws/lambda/internship-scraper --follow --region us-east-1
```

### Check Lambda Metrics

```bash
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=internship-scraper \
    --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 86400 \
    --statistics Sum \
    --region us-east-1
```

---

## Cost Estimate

**Monthly costs (assuming daily runs):**
- **Lambda:** ~$1-2/month (30 executions × 5 min × 2GB)
- **ECR:** ~$0.10/month (1GB image storage)
- **DynamoDB:** $0 (within free tier for low volume)
- **EventBridge:** $0 (first rule free)
- **Total:** ~$1-3/month

**Free Tier Benefits:**
- Lambda: 1M requests/month, 400,000 GB-seconds free
- DynamoDB: 25GB storage, 25 read/write units free
- ECR: 500MB storage free (your image is ~1GB)

---

## Troubleshooting

### Lambda Timeout Errors

**Symptom:** Function times out before completing.

**Solutions:**
1. Increase timeout (max 15 minutes):
   ```bash
   aws lambda update-function-configuration \
       --function-name internship-scraper \
       --timeout 900 \
       --region us-east-1
   ```

2. Optimize scraper code to run faster

### Chromium Crashes

**Symptom:** "Chromium crashed" or "browser not found" errors.

**Solutions:**
1. Increase memory (Chromium needs RAM):
   ```bash
   aws lambda update-function-configuration \
       --function-name internship-scraper \
       --memory-size 3008 \
       --region us-east-1
   ```

2. Check logs for specific errors:
   ```bash
   aws logs tail /aws/lambda/internship-scraper --region us-east-1
   ```

### DynamoDB Permission Errors

**Symptom:** "AccessDeniedException" when writing to DynamoDB.

**Solution:** Verify IAM role has DynamoDB permissions:
```bash
aws iam list-attached-role-policies --role-name lambda-scraper-role
```

Should include `AmazonDynamoDBFullAccess`.

### Docker Build Fails

**Symptom:** `deploy.sh` fails during Docker build.

**Solutions:**
1. Ensure Docker is running: `docker ps`
2. Check Dockerfile syntax
3. Verify dependencies in requirements.txt

### ECR Push Fails

**Symptom:** Authentication or permission errors when pushing to ECR.

**Solutions:**
1. Re-authenticate:
   ```bash
   aws ecr get-login-password --region us-east-1 | \
       docker login --username AWS --password-stdin \
       $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com
   ```

2. Verify AWS credentials: `aws sts get-caller-identity`

---

## Updating Configuration

### Change Schedule

Modify EventBridge cron expression:

**Examples:**
- Every 6 hours: `0 */6 * * ? *`
- Twice daily (9 AM & 9 PM): `0 9,21 * * ? *`
- Weekdays only: `0 9 ? * MON-FRI *`

```bash
aws events put-rule \
    --name daily-scraper-schedule \
    --schedule-expression "cron(NEW_EXPRESSION)" \
    --region us-east-1
```

### Update Environment Variables

```bash
aws lambda update-function-configuration \
    --function-name internship-scraper \
    --environment "Variables={
        DYNAMODB_TABLE_NAME=new-table-name,
        DISCORD_WEBHOOK_URL=new-webhook-url
    }" \
    --region us-east-1
```

---

## Cleanup / Deletion

To remove all AWS resources:

```bash
# Delete EventBridge rule
aws events remove-targets --rule daily-scraper-schedule --ids 1 --region us-east-1
aws events delete-rule --name daily-scraper-schedule --region us-east-1

# Delete Lambda function
aws lambda delete-function --function-name internship-scraper --region us-east-1

# Delete ECR repository
aws ecr delete-repository --repository-name internship-scraper --force --region us-east-1

# Delete DynamoDB table (WARNING: deletes all data)
aws dynamodb delete-table --table-name internships-jobs --region us-east-1

# Delete IAM role (detach policies first)
aws iam detach-role-policy --role-name lambda-scraper-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam detach-role-policy --role-name lambda-scraper-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
aws iam delete-role --role-name lambda-scraper-role
```

---

## Architecture Diagram

```
┌─────────────────────────────────────┐
│  EventBridge (Scheduler)            │
│  Cron: 0 9 * * ? *                 │
└───────────────┬─────────────────────┘
                │ triggers daily
                ▼
┌─────────────────────────────────────┐
│  Lambda Function                    │
│  - Docker container                 │
│  - Playwright + Chromium            │
│  - Your scraper code                │
└───────────┬─────────────────────────┘
            │ reads/writes
            ▼
┌─────────────────────────────────────┐
│  DynamoDB                           │
│  - internships-jobs table           │
│  - job_id (partition key)           │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│  Discord Webhook                    │
│  - Notifications for new jobs       │
└─────────────────────────────────────┘
```

---

## Support

For issues:
1. Check CloudWatch logs first
2. Review this troubleshooting guide
3. Verify AWS CLI commands execute without errors
4. Check AWS service status: https://status.aws.amazon.com

---

**Last updated:** 2026-02-12



# Simplified Explanation

- There are 2 main components:
    - Lambda - Function to run + specifications/permissions/variables
    - EventBridge - Scheduling and automation of Lambda function

- General flow:
    - Run deploy.sh to generate an image (3 entries) to ECR repo
        * Make sure docker desktop is running.*
    - Deploy the new image to Lambda
        - Out of the 3 recent images, SELECT THE MIDDLE ONE. This is the manifest. The index and metadata are not valid for deployment.
    - Test and check cloutdwatch logs