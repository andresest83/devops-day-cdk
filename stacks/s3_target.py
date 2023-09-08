from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3n
)

from constructs import Construct


class S3TargetStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, source_bucket_name=None, target_bucket_name=None, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)   

        # target_bucket = s3.CfnBucket(
        #     self,
        #     f"{target_bucket_name}-construct",
        #     bucket_name=f"{target_bucket_name}",
        #     versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(
        #         status="Enabled"
        #     )
        # )

        target_bucket = s3.Bucket(
            self, 
            f"{target_bucket_name}-construct",
            bucket_name = f"{target_bucket_name}",
            versioned=True,
        )

        bucket_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:ReplicateDelete",
                "s3:ReplicateObject",
                "s3:ObjectOwnerOverrideToBucketOwner",
                "s3:GetBucketVersioning",
                "s3:PutBucketVersioning"
            ],
            resources=[
                f"arn:aws:s3:::{target_bucket_name}",
                f"arn:aws:s3:::{target_bucket_name}/*"
            ],
            principals=[
                iam.ArnPrincipal(f"arn:aws:iam::{self.account}:role/S3CREncryptedReplicationRole"),
                iam.ArnPrincipal(f"arn:aws:iam::{self.account}:root")
            ]
        )

        # Add the bucket policy to the S3 bucket
        target_bucket.add_to_resource_policy(bucket_policy)
