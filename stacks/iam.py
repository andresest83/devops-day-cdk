from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3n
)

from constructs import Construct


class IamRoleStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, source_bucket_name=None, target_bucket_name=None, source_key_arn = None, target_key_arn = None, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        inline_policy_1 = iam.Policy(
                self,
                "InlinePolicy1",
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "s3:ListBucket",
                            "s3:GetReplicationConfiguration",
                            "s3:GetObjectVersionForReplication",
                            "s3:GetObjectVersionAcl",
                            "s3:GetObjectVersionTagging"
                        ],
                        resources=[
                            f"arn:aws:s3:::{source_bucket_name}",
                            f"arn:aws:s3:::{source_bucket_name}/*"
                        ],
                    )
                ],
                
        )

        inline_policy_2 = iam.Policy(
                self,
                "InlinePolicy2",
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "s3:ReplicateObject",
                            "s3:ReplicateDelete",
                            "s3:ReplicateTags"
                        ],
                        resources=[
                            f"arn:aws:s3:::{target_bucket_name}"
                        ],
                        conditions={
                            "StringLikeIfExists":{
                            "s3:x-amz-server-side-encryption":[
                                "aws:kms",
                                "AES256",
                                "aws:kms:dsse"
                            ],
                            "s3:x-amz-server-side-encryption-aws-kms-key-id":[
                                target_key_arn  
                            ]
                            }
                        }
                    )
                ],
                
        )

        inline_policy_3 = iam.Policy(
                self,
                "InlinePolicy3",
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "kms:Decrypt"
                        ],
                        resources=[
                            source_key_arn
                        ],
                        conditions={
                            "StringLike":{
                            "kms:ViaService":"s3.eu-central-1.amazonaws.com",
                            "kms:EncryptionContext:aws:s3:arn":[
                                f"arn:aws:s3:::{source_bucket_name}/*"
                            ]
                            }
                        }
                    )
                ],
                
        )

        inline_policy_4 = iam.Policy(
                self,
                "InlinePolicy4",
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "kms:Encrypt"
                        ],
                        resources=[
                            target_key_arn 
                        ],
                        conditions={
                            "StringLike":{
                            "kms:ViaService":"s3.us-east-1.amazonaws.com",
                            "kms:EncryptionContext:aws:s3:arn":[
                                f"arn:aws:s3:::{target_bucket_name}/*"
                            ]
                            }
                        }
                    )
                ],
                
        )

        replica_role = iam.Role(
            self,
            "CrossRegionReplicationRole",
            role_name="S3CREncryptedReplicationRole",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com"),
            inline_policies={
                "CrossRegionReplicationRolePolicy1": inline_policy_1.document,
                "CrossRegionReplicationRolePolicy2": inline_policy_2.document,
                "CrossRegionReplicationRolePolicy3": inline_policy_3.document,
                "CrossRegionReplicationRolePolicy4": inline_policy_4.document
            }
        )
