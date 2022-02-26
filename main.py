from init_aws_resources import *
from delete_aws_resources import *
from data_generator import generate_data
import time

# names of aws resources to be created
LAMBDA_ROLE_NAME = 'lambda_role'
STREAM_NAME = 'weather_stream'
TABLE_NAME = 'weather_table'
LAMBDA_FUNCTION_NAME = "save_to_dynomodb"


TIME_TO_LIVE=5*60 

# initialize AWS resources
def init_aws_resources():
    kinesis_arn = create_kinesis_stream(STREAM_NAME)
    print(kinesis_arn)

    dynamodb_table_arn = create_dynamodb_table(TABLE_NAME)
    print(dynamodb_table_arn)

    lambda_role_arn = create_lambda_role(LAMBDA_ROLE_NAME)
    print(lambda_role_arn)

    create_lambda_function(LAMBDA_FUNCTION_NAME, lambda_role_arn, kinesis_arn)
    print("AWS resources are created")

# Delete AWS resources
def delete_aws_resources():
    delete_kinesis_stream(STREAM_NAME)
    delete_lambda_role(LAMBDA_ROLE_NAME)
    delete_dynamodb_table(TABLE_NAME)
    delete_lambda_function(LAMBDA_FUNCTION_NAME)
    print("AWS resources are deleted")

# Main function
def main():

    init_aws_resources()

    generate_data(stream_name=STREAM_NAME)

    # wait N seconds before deleting aws rescources
    time.sleep(TIME_TO_LIVE)

    delete_aws_resources()


if __name__ == "__main__":
    main()
