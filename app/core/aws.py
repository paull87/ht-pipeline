import boto3

ec2 = boto3.resource('ec2', region_name='eu-west-2')

s3 = boto3.client('s3', region_name='eu-west-2')
