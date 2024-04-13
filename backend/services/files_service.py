import logging
import os
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile


AWS_S3_BUCKET = 'hectre-journals'
S3_FOLDER = f'uploads-{uuid4()}'
s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_S3_BUCKET)

logger = logging.getLogger(__name__)

def upload_file(file: UploadFile):
    key = os.path.join(S3_FOLDER, file.filename)
    
    try:
        # Upload the file to S3
        bucket.put_object(Key=key, Body=file.file)
    except ClientError as e:
        logger.error(e)
        return False
    return True
    
async def s3_download(key: str):
    try:
        return s3.Object(bucket_name=AWS_S3_BUCKET, key=key).get()['Body'].read()
    except ClientError as err:
        logger.error(str(err))