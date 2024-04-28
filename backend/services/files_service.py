import glob
from io import StringIO
import logging
import os
import time
import boto3

from typing import List, Optional, Tuple
from botocore.exceptions import ClientError
from fastapi import UploadFile
from pandas import DataFrame
from backend.consts import *
from hectre.api import extract_data
from hectre.cdf.cdf import CDF
from multiprocessing.pool import ThreadPool
import concurrent.futures

logger = logging.getLogger(__name__)


class FileS3Client:
    """S3 client to upload and download files from S3 bucket"""

    def __init__(self, region_name: str = REGION_NAME):
        self.s3 = boto3.resource("s3", region_name=region_name)
        self.bucket = self.s3.Bucket(AWS_S3_BUCKET)

    def upload_file(
        self, file: UploadFile, folder: str = S3_FOLDER_INPUT
    ) -> Tuple[bool, str]:
        """
        Uploads a file to S3 bucket
        Args:
            file: The file to upload
        Returns:
            Tuple of bool and str
        """
        key = os.path.join(folder, file.filename)

        try:
            # Upload the file to S3
            self.bucket.put_object(Key=key, Body=file.file)
        except ClientError as e:
            logger.error(e)
            return (False, "")
        return (True, folder)

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
            return (True, S3_FOLDER_INPUT)
        else:
            return (False, "")

    def list_buckets(self):
        """List all S3 buckets"""
        return [bucket.name for bucket in self.s3.buckets.all()]

    async def download_and_extract_files(
        self, in_folder: str, outcomes_string: str, out_folder: str = S3_FOLDER_OUTPUT
    ):
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

        def process_file(obj):

            local_file_path = os.path.join(local_dir, os.path.basename(obj.key))

            logger.info(f"local file path: {local_file_path}")

            self.bucket.download_file(obj.key, local_file_path)
            logger.info(f"Downloaded file: {obj.key} to {local_file_path}")

            logger.info(f"Invoking hectre API to extract data from {local_dir}")
            cdf: Optional[CDF] = extract_data(
                file_path=local_file_path, picos_string=outcomes_string
            )
            if cdf:
                df: DataFrame = cdf.to_df()
                filename = obj.key.split("/")[-1].split(".")[0] + ".csv"
                logger.info(f"saving object: {filename}")
                self.write_dataframe_to_s3(df, filename, out_folder)
            else:
                logger.error(
                    f"Could not get resulting CDF! Is the path correct: {local_dir}"
                )

        startime = time.time()
        # Create a ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Use list comprehension to start a thread for each object
            executor.map(process_file, self.bucket.objects.filter(Prefix=in_folder))

        endtime = time.time() - startime
        minutes, seconds = divmod(endtime, 60)
        logger.info(
            f"Total Extraction of all papers took: {minutes} min : {seconds} sec"
        )

        # Empty the temp folder
        self.remove_temp_dir(local_dir)

    def write_dataframe_to_s3(
        self, df: DataFrame, filename: str, folder: str = S3_FOLDER_OUTPUT
    ):
        """
        Writes a DataFrame to S3 bucket
        Args:
            df: The DataFrame to write
            bucket: The S3 bucket name
            key: The S3 key
        Returns:
            None
        """
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        key = os.path.join(folder, filename)
        logger.info(
            f"Writing DataFrame to S3 bucket folder: {folder} with filename: {filename}"
        )
        self.bucket.put_object(Key=key, Body=csv_buffer.getvalue())

    def remove_temp_dir(self, local_dir):
        """
        Removes all files in a directory
        Args:
            local_dir: The directory to empty
        Returns:
            None
        """
        files = glob.glob(os.path.join(local_dir, "*"))
        for f in files:
            os.remove(f)

        logger.info(f"Emptied the temp folder: {local_dir}")
