import boto3
import json
from zipfile import ZipFile



# create kinesis stream
def create_kinesis_stream(name: str):
    """
    Function creates AWS Kinesis Data Stream.

    Parameters
    --------------
    name : string
        Name of the data stream
    
    Returns
    --------------
    arn : string
        Amazon Resource Name (ARN)
    
    """
    kinesis = boto3.client('kinesis')
    streams = kinesis.list_streams()
    try:
        kinesis.create_stream(
            StreamName=name,
            ShardCount=1,
            StreamModeDetails={'StreamMode': 'PROVISIONED'}
        )
        print(f"Stream named {name} successfully created")
    except Exception as e:
        print(e)

    response = kinesis.describe_stream(StreamName=name)
    arn = response['StreamDescription']['StreamARN']
    return arn

# create dynamo db
def create_dynamodb_table(table_name: str):
    """
    Function creates DynamoDB table.

    Parameters
    --------------
    table_name : string
        Name of the DynamoDB table
    
    Returns
    --------------
    arn : string
        Amazon Resource Name (ARN)
    
    """
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

    table_info = dynamodb.describe_table(TableName=table_name)
    return table_info['Table']['TableArn']


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

# create lambda role
def create_lambda_role(role_name: str):
    """
    Function creates a role for AWS Lambda

    Parameters
    --------------
    role_name : string
        Name of the role
    
    Returns
    --------------
    arn : string
        Amazon Resource Name (ARN)
    
    """
    iam_client = boto3.client('iam')
    # create role itself
    try:
        iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_document)
    except Exception as e:
        print(e)

    # attach AWSLambdaKinesisExecutionRole policy
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole')
    except Exception as e:
        print(e)
    # attach AmazonDynamoDBFullAccess policy
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')
    except Exception as e:
        print(e)

    response = iam_client.get_role(RoleName=role_name)
    return response['Role']['Arn']

# convert zip file to binary to send to lambda function
def zip_to_binary(zipfile):
    with open(zipfile, 'rb') as file_data:
        bytes_content = file_data.read()
    return bytes_content


# Create Lambda function
def create_lambda_function(name, role_arn, kinesis_arn):
    """
    Function creates AWS Lambda function

    Parameters
    --------------
    name : string
        Name of the Lambda function
    
    role_arn : string
        ARN of Lambda role
    
    kinesis_arn : string
        ARN of Kinesis Data Stream
    """
    client = boto3.client('lambda')
    # zip the lambda.py
    ZipFile('lambda.zip', mode='w').write('lambda.py')
    
    # create lambda function
    try:
        client.create_function(
            FunctionName=name,
            Runtime='python3.9',
            Handler='lambda.lambda_handler',
            Role=role_arn,
            Code={"ZipFile": zip_to_binary('lambda.zip')}
        )
    except Exception as e:
        print(e)
    
    # add event soure mapping
    try:
        client.create_event_source_mapping(
            EventSourceArn=kinesis_arn,
            FunctionName=name,
            BatchSize=20,
            StartingPosition='TRIM_HORIZON')
    except Exception as e:
        print(e)
