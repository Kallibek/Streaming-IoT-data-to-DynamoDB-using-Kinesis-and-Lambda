import datetime
import boto3
import json
import random
import time

def generate_data(stream_name):
    kinesis = boto3.client('kinesis')
    while True:

        data = {
            'device_id': random.choice(['T001', 'T002', 'T003', 'T004']),
            'temperature': round((random.random()+1)*20, 2),
            'timestamp': datetime.datetime.now().isoformat()}
        response = kinesis.put_record(StreamName=stream_name,
                                      Data=json.dumps(data),
                                      PartitionKey=data['device_id'])
        print(f"Produced Record {response['SequenceNumber']}")

        time.sleep(0.5)
