from pathlib import Path
import os

from object_ai.storage.s3 import (create_labelbox_role,
                                  attach_bucket_cors_policy,
                                  create_labelbox_bucket_policy,
                                  create_bucket,
                                  attach_policy_to_role)
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.parent.joinpath('env', '.env')
load_dotenv(ENV_PATH)

bucket_name = 'object-ai-test-bucket2'
region = 'us-east-2'
response = create_bucket(bucket_name, region)
print(response)
response = create_labelbox_bucket_policy(bucket_name)
print(response)
response = attach_bucket_cors_policy(bucket_name)
print(response)
respone = create_labelbox_role('test-user',
                               aws_account_id=os.environ.get("LABELBOX_INTEGRATION_AWS_ACCOUNT"),
                               external_id=os.environ.get("LABELBOX_INTEGRATION_EXTERNAL_ID"))
print(respone)
response = attach_policy_to_role('LabelboxAWSAccounttest-user',
                                 f'arn:aws:iam::{os.environ.get("AWS_ACCOUNT_ID")}:policy/LabelboxReadobject-ai-test-bucket2')
print(response)