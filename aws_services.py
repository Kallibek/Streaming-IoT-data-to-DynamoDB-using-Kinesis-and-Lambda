import boto3
import json

LAMBDA_ROLE_NAME = 'lambda_role_to_read_data_stream'

# create kinesis stream

def create_kinesis_stream(name:str):
    kinesis = boto3.client('kinesis')
    stream = kinesis.list_streams()
    if name in stream['StreamNames']:
        print(f"Stream named {name} already exists")
        pass
    else:
        kinesis.create_stream(
        StreamName=name,
        ShardCount=1,
        StreamModeDetails={'StreamMode': 'PROVISIONED'}
        )
        print(f"Stream named {name} successfully created")

# create a role for Lambda
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
# arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess

# iam = boto3.resource('iam')
# role = iam.Role('lambda_role_to_read_data_stream')
# role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess')
assume_role_policy_document = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
    ]
})

iam_client = boto3.client('iam')
iam_client.create_role(
    RoleName=LAMBDA_ROLE_NAME,
    AssumeRolePolicyDocument=assume_role_policy_document
)
iam_client.attach_role_policy(
    RoleName=LAMBDA_ROLE_NAME,
    PolicyArn='arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess')

iam_client.attach_role_policy(
    RoleName=LAMBDA_ROLE_NAME,
    PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')
# arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
# Create Lambda function
# lambda_client = boto3.client('lambda')
# lambda_client.create_function(FunctionName="Consumer")
# create dynamo db

# delete kinesis stream
def delete_kinesis_stream(name:str):
    kinesis = boto3.client('kinesis')
    stream = kinesis.list_streams()
    if name in stream['StreamNames']:
        kinesis.delete_stream(StreamName=name)
        print(f"Stream named {name} successfully deleted")
    else:
        print(f"Stream named {name} doesn't exist")
# delete Lambda function

# delete dynamo db