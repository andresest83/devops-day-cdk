from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
)

from constructs import Construct


class S3SourceStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str,source_bucket_name=None,target_bucket_name=None,**kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        replication_configuration_property = s3.CfnBucket.ReplicationConfigurationProperty(
            role=f"arn:aws:iam::{self.account}:role/S3CREncryptedReplicationRole",
            rules=[
                s3.CfnBucket.ReplicationRuleProperty(
                    status="Enabled",
                    destination=s3.CfnBucket.ReplicationDestinationProperty(
                            bucket=f"arn:aws:s3:::{target_bucket_name}",
                    ),
                )
            ],
        )

        source_bucket = s3.CfnBucket(
            self,
            f"{source_bucket_name}-construct",
            bucket_name=f"{source_bucket_name}",
            versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(
                status="Enabled"
            ),
            replication_configuration=replication_configuration_property                 
        )

        
