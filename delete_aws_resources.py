import boto3
# delete kinesis stream


def delete_kinesis_stream(name: str):
    """
    Function deletes AWS Kinesis Data Stream.

    Parameters
    --------------
    name : string
        Name of the data stream
    """
    kinesis = boto3.client('kinesis')
    try:
        kinesis.delete_stream(StreamName=name)
    except Exception as e:
        print(e)



def delete_lambda_role(role_name: str):
    """
    Function deletes AWS Lambda role.

    Parameters
    --------------
    role_name : string
        Name of AWS Lambda role
    """
    iam_client = boto3.client('iam')
    # detach attached policies
    try:
        iam_client.detach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole')
    except Exception as e:
        print(e)
    try:
        iam_client.detach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')
    except Exception as e:
        print(e)
    
    # then delete the role
    try:
        iam_client.delete_role(
            RoleName=role_name)
    except Exception as e:
        print(e)




# delete dynamo db
def delete_dynamodb_table(table_name: str):
    """
    Function deletes DynamoDB table

    Parameters
    --------------
    table_name : string
        Name of DynamoDB table
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.delete()




# delete Lambda function
def delete_lambda_function(name):
    """
    Function deletes AWS Lambda function

    Parameters
    --------------
    name : string
        Name of AWS Lambda function
    """
    client = boto3.client('lambda')
    client.delete_function(FunctionName=name)
