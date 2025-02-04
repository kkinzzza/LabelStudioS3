# Local LabelStudio Environment with S3-like Storage
## Introduction
This project is a code for deploying (with Docker containers) LabelStudio data markup environment on the local machine with connected S3-like object storage powered by MiniO. The main idea is to integrate S3 storage to the pipeline of data markup for better organization of data which are being processed. S3-like storage is using for import and export data for labeling them in LabelStudio environment.

The perspectives of this idea connect with integrating this soft into ML projects which use custom hand-labeled datasets.

## Usage
There're 4 steps which you need to do for deploying:

1.  Install required packages:

    ```
    pip install boto3==1.36.5 label-studio==1.15.0
    ```
    
2.  Run `storage_init.py` for MiniO storage initialization:

    ```
    python storage_init.py
    ```

    After running this code you will get such an answer if it's OK:
    
    ```
    Storage initialized.
    Bucket label-studio already exists.
    Bucket Policy Set to Public.
    ```

    MiniO S3-like storage will be working on `http://localhost:9000` (console will be on `http://localhost:9001`).
    
3.  Run `ls_init.py` for LabelStudio environment initialization:

    ```
    python ls_init.py
    ```

    After running this code you will get such an answer if it's OK:
    
    ```
    Label Studio Initialized.
    Enter the token:
    ```

4.  Enter the API token from LabelStudio, working on `http://localhost:8080` and press Enter.
5.  After pressing Enter button the project will be created and the S3 storage will be connected with project in deployed LabelStudio environment. If it's OK, the response will be the following:
    ```
    Project Making OK.
    Connecting to http://localhost:9000…
    Storage connected to Project <Project Title> successfully.
    ```

## Result
MiniO S3-like storage and LabelStudio environment are deployed on the local machine and located on 3 addresses: 9000 and 9001 ports of `http://localhost` are related to MiniO and 8080 port is for LabelStudio. Also there's a project in LabelStudio which is connected to the MiniO storage. 

## Possible Perspectives
This code can be modified to a code for making more projects in LabelStudio, buckets in MiniO storage and connect them between each other. 

    
