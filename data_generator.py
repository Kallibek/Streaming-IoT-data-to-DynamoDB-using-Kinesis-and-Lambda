import datetime
import boto3
import json
import logging
import random
import time


while True:
    kinesis = boto3.client('kinesis')
    data={
            'ticker':random.choice(['tqqq','soxl','tecl','btc','spxl']),
            'price':round(random.random()*100,2),
            'timestamp':datetime.datetime.now().isoformat()}
    response = kinesis.put_record(StreamName=stream_name,
                                        Data=json.dumps(data),
                                        PartitionKey='1')
    print(f"Produced Record {response['SequenceNumber']}")
    time.sleep(1)
    
