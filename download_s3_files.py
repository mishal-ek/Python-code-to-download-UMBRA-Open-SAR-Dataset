import boto3
import os
from botocore import UNSIGNED
from botocore.config import Config

# Configuration
bucket_name = 'umbra-open-data-catalog'
prefix = ''  # Update this if you want to narrow down the search
local_download_path = r'path\to\umbra_data'  # Update this path

# Create a boto3 client with no AWS credentials
s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Create a local directory to store downloaded files
if not os.path.exists(local_download_path):
    os.makedirs(local_download_path)

def download_file(bucket, key, download_path):
    local_filename = os.path.join(download_path, key)
    if not os.path.exists(os.path.dirname(local_filename)):
        os.makedirs(os.path.dirname(local_filename))
    s3_client.download_file(bucket, key, local_filename)

def main():
    paginator = s3_client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_name, 'Prefix': prefix}
    
    for page in paginator.paginate(**operation_parameters):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if key.endswith('.tif') or key.endswith('.json'):
                    print(f'Downloading {key}')
                    download_file(bucket_name, key, local_download_path)

if __name__ == "__main__":
    main()
