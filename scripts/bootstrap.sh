# SIMPLE
cdk bootstrap -c @aws-cdk/core:newStyleStackSynthesis=true --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess aws://ACCOUNT/REGION

# TRUST ANOTHER ACCOUNT
cdk bootstrap --trust SOURCEACCOUNT -c @aws-cdk/core:newStyleStackSynthesis=true --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess aws://TARGETACCOUNT/REGION
