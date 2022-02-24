import boto3

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