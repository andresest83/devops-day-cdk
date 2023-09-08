#!/usr/bin/env python3
#env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

import aws_cdk as cdk
import os

from stacks.s3_source import S3SourceStack
from stacks.s3_target import S3TargetStack
from stacks.iam import IamRoleStack

app = cdk.App()

# VARIABLES
account = os.getenv('CDK_DEFAULT_ACCOUNT')
source_region = "eu-central-1"
target_region = "us-east-1"
source_bucket_name = ""
target_bucket_name = ""
source_key_arn = ""
target_key_arn = ""

# STACKS
iam_source = IamRoleStack(
    app,
    "DBC-IAMSourceStack",
    source_bucket_name=source_bucket_name,
    target_bucket_name=target_bucket_name,
    source_key_arn = source_key_arn,
    target_key_arn = target_key_arn,
    env=cdk.Environment(account=account, region=source_region),
)

s3_source = S3SourceStack(
    app,
    "DBC-S3Sourcetack",
    source_bucket_name=source_bucket_name,
    target_bucket_name=target_bucket_name,
    target_region = target_region,
    target_key_arn = target_key_arn,
    env=cdk.Environment(account=account, region=source_region),
)

s3_target = S3TargetStack(
    app,
    "DBC-S3TargetStack",
    source_bucket_name=source_bucket_name,
    target_bucket_name=target_bucket_name,
    env=cdk.Environment(account=account, region=target_region),
)

s3_target.add_dependency(iam_source)
s3_source.add_dependency(s3_target)

app.synth()
