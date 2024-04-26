import glob
import logging
import os
import time
import boto3

from typing import List, Optional, Tuple
from botocore.exceptions import ClientError
from fastapi import UploadFile
from backend.consts import *
from hectre.api import extract_data
from hectre.cdf.cdf import CDF
from multiprocessing.pool import ThreadPool


logger = logging.getLogger(__name__)


class FileS3Client:
    """S3 client to upload and download files from S3 bucket"""

    def __init__(self, region_name: str = REGION_NAME):
        self.s3 = boto3.resource("s3", region_name=region_name)
        self.bucket = self.s3.Bucket(AWS_S3_BUCKET)

    def upload_file(self, file: UploadFile) -> Tuple[bool, str]:
        """
        Uploads a file to S3 bucket
        Args:
            file: The file to upload
        Returns:
            Tuple of bool and str
        """
        key = os.path.join(S3_FOLDER, file.filename)

        try:
            # Upload the file to S3
            self.bucket.put_object(Key=key, Body=file.file)
        except ClientError as e:
            logger.error(e)
            return (False, "")
        return (True, S3_FOLDER)

    def upload_files(self, files: List[UploadFile]) -> Tuple[bool, str]:
        """
        Uploads multiple files to S3 bucket
        Args:
            files: List of files to upload
        Returns:
            Tuple of bool and str
        """
        pool = ThreadPool(len(files))

        startime = time.time()
        results = pool.map(self.upload_file, files)
        endtime = time.time() - startime

        pool.close()

        if all(results):
            logger.debug(f"all {len(files)} files uploaded in : {endtime} seconds")
            return (True, S3_FOLDER)
        else:
            return (False, "")

    def list_buckets(self):
        """List all S3 buckets"""
        return [bucket.name for bucket in self.s3.buckets.all()]

    async def download_and_extract_files(self, folder_name: str, outcomes_string: str):
        """
        Downloads a file from S3 bucket,
        saves to a temporary directory,
        and invokes hectre API to extract data.
        Args:
            folder_name: The folder name in S3 bucket
            outcomes_string: The outcomes string
        Returns:
            None
        """
        cwd = os.getcwd()
        local_dir = os.path.join(cwd, TEMP_DIR)

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        try:
            for obj in self.bucket.objects.filter(Prefix=folder_name):

                local_file_path = os.path.join(local_dir, os.path.basename(obj.key))

                logger.info(f"local file path: {local_file_path}")

                self.bucket.download_file(obj.key, local_file_path)
                logger.info(f"Downloaded file: {obj.key} to {local_file_path}")

                startime = time.time()
                logger.info(f"Invoking hectre API to extract data from {local_dir}")

                cdf: Optional[CDF] = extract_data(
                    file_path=local_file_path, picos_string=outcomes_string
                )
                if cdf:
                    output_filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    cdf.save_to_file(output_filename)
                else:
                    logger.error(
                        f"Could not get resulting CDF! Is the path correct: {local_dir}"
                    )

                endtime = time.time() - startime
                logger.info(f"Extraction took: {endtime} seconds")

        except ClientError as e:
            logger.error(e)

        # Empty the temp folder
        self.new_method(local_dir)

    def new_method(self, local_dir):
        files = glob.glob(os.path.join(local_dir, "*"))
        for f in files:
            os.remove(f)

        logger.info(f"Emptied the temp folder: {local_dir}")
