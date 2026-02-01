"""
Database Manager - Handles all DynamoDB operations
"""
import boto3
from datetime import datetime
from config import DYNAMODB_TABLE_NAME


class DBManager:
    def __init__(self):
        """Initialize DynamoDB connection"""
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(DYNAMODB_TABLE_NAME)

    def get_active_jobs(self, source_id):
        """
        Get all active jobs for a specific source from DynamoDB

        Args:
            source_id (str): The source identifier (e.g., 'lever_anthropic')

        Returns:
            dict: Dictionary mapping job_id to job item
        """
        response = self.table.scan(
            FilterExpression='source = :source AND #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':source': source_id, ':status': 'active'}
        )
        return {item['job_id']: item for item in response['Items']}

    def insert_job(self, job):
        """
        Insert new job into DynamoDB

        Args:
            job (dict): Job dictionary containing all job details
        """
        self.table.put_item(Item=job)

    def update_last_seen(self, job_id):
        """
        Update last_seen timestamp for existing job

        Args:
            job_id (str): The job identifier
        """
        self.table.update_item(
            Key={'job_id': job_id},
            UpdateExpression='SET last_seen = :timestamp',
            ExpressionAttributeValues={':timestamp': datetime.utcnow().isoformat()}
        )

    def mark_as_removed(self, job_id):
        """
        Mark job as removed (no longer available)

        Args:
            job_id (str): The job identifier
        """
        self.table.update_item(
            Key={'job_id': job_id},
            UpdateExpression='SET #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'removed'}
        )
