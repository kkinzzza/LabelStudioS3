import subprocess
import os
import env_params as envp
import label_studio_sdk as ls

def init(port, username, password):
    container = [
        "docker", "run", "-d", "--name", "labelstudio",
        "-p", f"{port}:8080",
        "-e", f"USERNAME={username}",
        "-e", f"PASSWORD={password}",
        "heartexlabs/label-studio:latest"
    ]

    try:
        subprocess.run(container, check=True)
        print('Label Studio Initialized.')
    except subprocess.CalledProcessError as e:
        print(f"Label Studio Initializing Error: {e}")

def storage_connect(port, api_token, storage_port, storage_access_key, storage_secret_key, bucket_name):
    client = ls.Client(
        url=f'http://localhost:{port}',
        api_key=api_token
    )

    project = client.create_project(
        title='Test_Project_1'
    )
    print('Project Making OK.')

    # Подключение S3 хранилища
    print(f'Connecting to http://localhost:{storage_port}…')
    try:
        project.connect_s3_import_storage(
            bucket=bucket_name,
            use_blob_urls=True,
            aws_access_key_id=storage_access_key,
            aws_secret_access_key=storage_secret_key,
            s3_endpoint=f'http://host.docker.internal:{storage_port}'
        )
        print(f"Storage connected to Project {project.title} successfully.")
    except Exception as e:
        print(f'Storage Connection Failed: {e}')

if __name__ == '__main__':
    init(
        port=envp.port,
        username=envp.username,
        password=envp.password
    )

    token = input('Enter the token: ')

    storage_connect(
        port=envp.port,
        api_token=token,
        storage_port=envp.storage_port,
        storage_access_key=envp.storage_access_key,
        storage_secret_key=envp.storage_secret_key,
        bucket_name=envp.bucket
    )