import base64
import boto3
import json
from decimal import Decimal

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    for record in event['Records']:
        data=base64.b64decode(record["kinesis"]["data"])
        data=json.loads(data, parse_float=Decimal)
        table = dynamo.Table('weather_table')
        table.put_item(Item=data)