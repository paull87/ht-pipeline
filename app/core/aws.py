import boto3
import boto3
import logging
import json
from app.settings.secrets import REGION, ACCOUNT_ID, PL_AWS_ACCESS_KEY, PL_SECRET_ACCESS_KEY

ec2 = boto3.resource('ec2', region_name='eu-west-2')

s3 = boto3.client('s3', region_name='eu-west-2')

# Currently set to use mine as it has the lambda/sns
sns = boto3.client(
    'sns',
    region_name='eu-west-1',
    aws_access_key_id=PL_AWS_ACCESS_KEY,
    aws_secret_access_key=PL_SECRET_ACCESS_KEY,
)


def publish_sns(command, payload):
    topic_arn = f'arn:aws:sns:{REGION}:{ACCOUNT_ID}:{command}'
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(payload))
        return response
    except Exception as e:
        return f'ERROR {e}'
