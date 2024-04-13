import logging
import os
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from datetime import datetime
from backend.consts import *

S3_FOLDER = f'uploads-{datetime.now().strftime(DATETIME_FMT)}'
s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_S3_BUCKET)

logger = logging.getLogger(__name__)

def upload_file(file: UploadFile):
    """Uploads a file to S3 bucket"""
    key = os.path.join(S3_FOLDER, file.filename)
    
    try:
        # Upload the file to S3
        bucket.put_object(Key=key, Body=file.file)
    except ClientError as e:
        logger.error(e)
        return False
    return True
    
async def s3_download(key: str):
    """Downloads a file from S3 bucket"""
    try:
        return s3.Object(bucket_name=AWS_S3_BUCKET, key=key).get()['Body'].read()
    except ClientError as err:
        logger.error(str(err))