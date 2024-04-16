import logging
import os
import time
from typing import List
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from consts import *
from multiprocessing.pool import ThreadPool


logger = logging.getLogger(__name__)


class FileS3Client:
    """S3 client to upload and download files from S3 bucket"""

    def __init__(self, region_name: str = REGION_NAME):
        self.s3 = boto3.resource("s3", region_name=region_name)
        self.bucket = self.s3.Bucket(AWS_S3_BUCKET)

    def upload_file(self, file: UploadFile) -> bool:
        """Uploads a file to S3 bucket"""
        key = os.path.join(S3_FOLDER, file.filename)

        try:
            # Upload the file to S3
            self.bucket.put_object(Key=key, Body=file.file)
        except ClientError as e:
            logger.error(e)
            return False
        return True

    def upload_files(self, files: List[UploadFile]) -> bool:
        """Uploads multiple files to S3 bucket"""
        pool = ThreadPool(len(files))

        startime = time.time()
        results = pool.map(self.upload_file, files)
        endtime = time.time() - startime

        pool.close()

        if all(results):
            logger.debug(f"all {len(files)} files uploaded in : {endtime} seconds")
            return True
        else:
            return False

    def list_buckets(self):
        """List all S3 buckets"""
        return [bucket.name for bucket in self.s3.buckets.all()]

    async def download_file(self, key: str):
        """Downloads a file from S3 bucket"""
        try:
            return (
                self.s3.Object(bucket_name=AWS_S3_BUCKET, key=key).get()["Body"].read()
            )
        except ClientError as err:
            logger.error(str(err))
