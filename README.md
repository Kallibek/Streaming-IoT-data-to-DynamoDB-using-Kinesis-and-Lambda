# Streaming IoT data to DynamoDB using Kinesis and Lambda

by Kallibek Kazbekov

date: Feb 25, 2022

# Summary
This project builds a pipeline that uploads streaming data from Kinesis Data Stream to DynamoDB using AWS Lambda.

![Data pipeline](pipeline.png)

The data generator imitates IoT devices that stream real-time temperature data to the Kinesis Data Stream, which triggers a Lambda function that writes observations to the DynamoDB table for further analysis by data analysts.

# Packages
Project is created with:
* boto3 version: 1.20.44
* botocore version: 1.23.48
	
# Setup
Before running the project make sure the AWS user creadentials are set as environmental variables. To run this project, install the requirements and then execute:

```python main.py```
