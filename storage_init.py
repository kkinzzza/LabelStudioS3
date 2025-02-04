import subprocess
import os
import storage_params as stp
import boto3
import json

def init(storage_name, storage_port, console_port, access_key, secret_key, local_path, bucket_name):
    path = os.path.expanduser(local_path)
    os.makedirs(path, exist_ok=True)

    container = [
        'docker', 'run', '-d', '--name', 'miniostorage',
        '-p', f'{storage_port}:9000', '-p', f'{console_port}:9001',
        '-e', f'MINIO_ROOT_USER={access_key}',
        '-e', f'MINIO_ROOT_PASSWORD={secret_key}',
        '-v', f'{path}:/data',
        'quay.io/minio/minio', 'server', '/data', '--console-address', f':{console_port}'
    ]

    try:
        subprocess.run(container, check=True)
        print('Storage initialized.')
    except subprocess.CalledProcessError as e:
        print(f'Storage Initializing Error: {e}')

    client = boto3.client(
        's3',
        endpoint_url=f'http://localhost:{storage_port}',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    try:
        existing_buckets = client.list_buckets()['Buckets']
        if any(bucket['Name'] == bucket_name for bucket in existing_buckets):
            print(f'Bucket {bucket_name} already exists.')
        else:
            client.create_bucket(Bucket=bucket_name)
            print(f'Bucket {bucket_name} made successfully.')
    except Exception as e:
        print(f'Bucket Making Error: {e}')

    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Principal': {
                    'AWS': [
                        '*'
                    ]
                },
                'Action': [
                    's3:ListBucket',
                    's3:ListBucketMultipartUploads',
                    's3:GetBucketLocation'
                ],
                'Resource': [
                    'arn:aws:s3:::label-studio'
                ]
            },
            {
                'Effect': 'Allow',
                'Principal': {
                    'AWS': [
                        '*'
                    ]
                },
                'Action': [
                    's3:AbortMultipartUpload',
                    's3:DeleteObject',
                    's3:GetObject',
                    's3:ListMultipartUploadParts',
                    's3:PutObject'
                ],
                'Resource': [
                    'arn:aws:s3:::label-studio/*'
                ]
            }
        ]
    }

    try:
        client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(policy)
        )
        print('Bucket Policy Set to Public.')
    except Exception as e:
        print(f'Bucket Policy Updating Error: {e}')

if __name__ == '__main__':
    init(
        storage_name=stp.storage_name,
        bucket_name=stp.bucket_name,
        storage_port=stp.storage_port,
        console_port=stp.console_port,
        access_key=stp.access_key,
        secret_key=stp.secret_key,
        local_path=stp.directory_path
    )