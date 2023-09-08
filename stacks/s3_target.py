from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
)

from constructs import Construct


class S3TargetStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, source_bucket_name=None,target_bucket_name=None,**kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        target_bucket = s3.Bucket(
            self, 
            f"{target_bucket_name}-construct",
            bucket_name = f"{target_bucket_name}",
            versioned=True,
        )
