import json
import logging

import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            response = s3_client.create_bucket(Bucket=bucket_name,
                                               CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return None
    return response


def attach_bucket_cors_policy(bucket_name):
    # Define the configuration rules
    cors_configuration = {
        'CORSRules': [
        {
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "GET"
            ],
            "AllowedOrigins": [
                "https://app.labelbox.com",
                "https://editor.labelbox.com"
            ],
            "ExposeHeaders": []
        }
    ]
    }

    # Set the CORS configuration
    s3 = boto3.client('s3')
    try:
        response = s3.put_bucket_cors(Bucket=bucket_name,
                                      CORSConfiguration=cors_configuration)
    except ClientError as e:
        logging.error(e)
        return None
    return response


def create_labelbox_role(user_id, aws_account_id, external_id):
    client = boto3.client('iam')
    trust_relationship_policy_another_iam_user = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Principal": {
                    "AWS": aws_account_id
                },
                "Condition": {
                    "StringEquals": {
                        "sts:ExternalId": external_id
                    }
                }
            }
        ]
    }
    try:
        response = client.create_role(
            RoleName=f'LabelboxAWSAccount{user_id}',
            AssumeRolePolicyDocument=json.dumps(trust_relationship_policy_another_iam_user),
            Description='Trust Labelbox aws account'
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response


def attach_policy_to_role(role_name, policy_arn):
    client = boto3.client('iam')
    try:
        response = client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response


def create_labelbox_bucket_policy(bucket_name):
    client = boto3.client('iam')
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    # Convert the policy from JSON dict to string
    policy_document = json.dumps(policy)
    try:
        response = client.create_policy(
            PolicyName=f'LabelboxRead{bucket_name}',
            PolicyDocument=policy_document,
            Description='Give labelbox read access to bucket',
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response

