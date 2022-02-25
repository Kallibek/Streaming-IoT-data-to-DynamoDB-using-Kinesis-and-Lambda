from tkinter import E
import boto3
import json
import base64
from zipfile import ZipFile

LAMBDA_ROLE_NAME = 'lambda_role_to_read_data_stream'
STREAM_NAME = 'Weather'
TABLE_NAME = 'weather'
LAMBDA_FUNCTION_NAME = "save_2_dynomodb"
# create kinesis stream


def create_kinesis_stream(name: str):
    kinesis = boto3.client('kinesis')
    streams = kinesis.list_streams()

    if name in streams['StreamNames']:
        print(f"Stream named {name} already exists")
        response = kinesis.describe_stream(StreamName=name)
    else:
        response = kinesis.create_stream(
            StreamName=name,
            ShardCount=1,
            StreamModeDetails={'StreamMode': 'PROVISIONED'}
        )
        print(f"Stream named {name} successfully created")

    response = kinesis.describe_stream(StreamName=name)
    arn = response['StreamDescription']['StreamARN']
    return arn


kinesis_arn=create_kinesis_stream(STREAM_NAME)
print(kinesis_arn)

# create dynamo db

def create_dynamodb_table(table_name: str):
    try:
        dynamodb = boto3.client('dynamodb')
        dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'device_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'
                }

            ],
            KeySchema=[
                {
                    'AttributeName': 'device_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
    except Exception as e:
        print(e)

    table_info=dynamodb.describe_table(TableName=table_name)
    return table_info['Table']['TableArn']


table_arn = create_dynamodb_table(TABLE_NAME)
print(table_arn)

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

def create_lambda_role(role_name: str):
    iam_client = boto3.client('iam')
    try:
        iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_document)
    except Exception as e:
        print(e)

    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole')
    except Exception as e:
        print(e)
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')
    except Exception as e:
        print(e)
    response  = iam_client.get_role(RoleName=role_name)
    return response['Role']['Arn']
    

lambda_role_arn = create_lambda_role(LAMBDA_ROLE_NAME)
print(lambda_role_arn)

# 

def zip_to_binary(zipfile):
    with open(zipfile, 'rb') as file_data:
        bytes_content = file_data.read()
    return bytes_content
# Create Lambda function
def create_lambda_function(name, role_arn):
    client = boto3.client('lambda')
    # zip the lambda.py
    ZipFile('lambda.zip', mode='w').write('lambda.py') 
    try:
        response = client.create_function(
            FunctionName=name,
            Runtime='python3.9',
            Handler='lambda.lambda_handler',
            Role = role_arn,
            Code = {"ZipFile":zip_to_binary('lambda.zip')}
        )
    except Exception as e:
        print(e)
    try:
        response = client.create_event_source_mapping(
            EventSourceArn=kinesis_arn,
            FunctionName=name,
            BatchSize=20,
            StartingPosition='TRIM_HORIZON')
    except Exception as e:
        print(e)

create_lambda_function(LAMBDA_FUNCTION_NAME,lambda_role_arn)
# delete kinesis stream


def delete_kinesis_stream(name: str):
    kinesis = boto3.client('kinesis')
    stream = kinesis.list_streams()
    if name in stream['StreamNames']:
        kinesis.delete_stream(StreamName=name)
        print(f"Stream named {name} successfully deleted")
    else:
        print(f"Stream named {name} doesn't exist")

# delete lambda role
delete_kinesis_stream(STREAM_NAME)

def delete_lambda_role(role_name: str):
    iam_client = boto3.client('iam')
    try:
        iam_client.detach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess')

        iam_client.detach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')

        iam_client.delete_role(
            RoleName=role_name)

    except:
        print("Error in deleting a lambda role")


delete_lambda_role(LAMBDA_ROLE_NAME)
# delete Lambda function

# delete dynamo db


def delete_dynamodb_table(table_name: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.delete()


delete_dynamodb_table(TABLE_NAME)
