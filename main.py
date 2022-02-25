from aws_services import *
STREAM_NAME='Weather'
LAMBDA_ROLE_NAME = 'lambda_role_to_read_data_stream'
TABLE_NAME = 'weather'
def init_aws_services():
    create_kinesis_stream(STREAM_NAME)
    
def generate_data():
    pass
def main():
    init_aws_services()
    
    generate_data()
    pass

if __name__ == "__main__":
    main()

