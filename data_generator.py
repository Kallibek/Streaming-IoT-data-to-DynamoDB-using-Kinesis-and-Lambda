import datetime
import boto3
import json
import random
import time

STREAM_NAME = 'Weather'


def generate_data(StreamName):
    kinesis = boto3.client('kinesis')
    while True:
        
        data = {
            'device_id': random.choice(['T001', 'T002', 'T003', 'T004']),
            'temperature': round((random.random()+1)*20, 2),
            'timestamp': datetime.datetime.now().isoformat()}
        response = kinesis.put_record(StreamName=StreamName,
                                      Data=json.dumps(data),
                                      PartitionKey=data['device_id'])
        print(f"Produced Record {response['SequenceNumber']}")
        
        time.sleep(1)
        
generate_data('Weather')

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('weather')
table.put_item(Item={"device_id":"12ds","temperature": 1, "timestamp":"Now"})


