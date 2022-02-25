import boto3
import json

LAMBDA_ROLE_NAME = 'lambda_role_to_read_data_stream'
STREAM_NAME = 'Weather'
TABLE_NAME = 'weather'
# create kinesis stream


def create_kinesis_stream(name: str):
    kinesis = boto3.client('kinesis')
    streams = kinesis.list_streams()

    if name in streams['StreamNames']:
        print(f"Stream named {name} already exists")
        response = kinesis.describe_stream(StreamName=name)
        arn = response['StreamDescription']['StreamARN']
        pass
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


create_kinesis_stream(STREAM_NAME)

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

        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess')

        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')
    except:
        print("Error in creating a lambda role")


create_lambda_role(LAMBDA_ROLE_NAME)


# Create Lambda function
def create_lambda_function():
    pass


create_lambda_function()

# lambda_client = boto3.client('lambda')
# lambda_client.create_function(FunctionName="Consumer")
# create dynamo db


def create_dynamodb_table(table_name: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
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
            'ReadCapacityUnits': 2,
            'WriteCapacityUnits': 2
        }
    )
    return table


create_dynamodb_table(TABLE_NAME)

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
