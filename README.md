# devops-day-cdk

Teaching example from an internal AWS DevOps Day session in 2023: cross-region S3
replication of KMS-encrypted objects, in AWS CDK (Python).

Built for a room of about 50 new joiners learning CDK. The code is deliberately small so
the moving parts stay visible. Archived as written, not maintained, not a production
starting point.

## What it builds

| Stack | Region | Contents |
| --- | --- | --- |
| `DBC-IAMSourceStack` | source | Replication role and its inline policies |
| `DBC-S3Sourcetack` | source | Versioned source bucket carrying the replication rule |
| `DBC-S3TargetStack` | target | Versioned target bucket and its bucket policy |

Defaults to `eu-central-1` replicating into `us-east-1`.

## Why SSE-KMS is the interesting case

Replicating unencrypted objects is a checkbox. Replicating KMS-encrypted ones needs three
things to line up, and if any is missing, replication skips the objects silently instead
of failing:

1. `SourceSelectionCriteria.SseKmsEncryptedObjects` set to `Enabled`. Without it S3 ignores
   encrypted objects rather than erroring.
2. `EncryptionConfiguration.ReplicaKmsKeyID` pointing at a key in the *target* region. KMS
   keys are regional, so the source key cannot be reused.
3. A replication role with `kms:Decrypt` on the source key and `kms:Encrypt` on the target
   key, on top of the usual S3 permissions.

Versioning on both buckets is a hard requirement, not a recommendation.

## Usage

Set the variables at the top of `app.py` (bucket names, KMS key ARNs, regions), then:

```bash
./scripts/create_keys.sh    # KMS keys in both regions, policy in key-policy.json
./scripts/bootstrap.sh      # cdk bootstrap, including cross-account trust
cdk deploy DBC-IAMSourceStack
cdk deploy DBC-S3Sourcetack
cdk deploy DBC-S3TargetStack
```

Order matters: the source bucket's replication rule references the role by ARN.

## Licence

Apache-2.0. See [LICENSE](LICENSE).
