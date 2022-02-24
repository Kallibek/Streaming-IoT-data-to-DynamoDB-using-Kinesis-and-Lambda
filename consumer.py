import boto3
import json

kinesis = boto3.client('kinesis')
stream_name = 'custom_stream'

response = kinesis.describe_stream(StreamName=stream_name)

shard_id=response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator = kinesis.get_shard_iterator(StreamName=stream_name,
                                                      ShardId=shard_id,
                                                      ShardIteratorType='TRIM_HORIZON')

my_shard_iterator = shard_iterator['ShardIterator']

record_response = kinesis.get_records(ShardIterator=my_shard_iterator)
print(record_response['Records'][-1])