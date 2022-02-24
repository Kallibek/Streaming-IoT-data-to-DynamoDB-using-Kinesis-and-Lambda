from aws_services import *
STREAM_NAME='Weather'

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

