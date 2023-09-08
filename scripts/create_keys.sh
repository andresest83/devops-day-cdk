aws kms create-key --description source_key_name--policy file://key-policy.json --region eu-central-1
aws kms create-key --description target_key_name --policy file://key-policy.json --region us-east-1
