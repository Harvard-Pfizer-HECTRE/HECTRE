import boto3
import os
import pytest

from moto import mock_aws
from consts import REGION_NAME


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.getenv("AWS_ACCESS_KEY_ID")
    os.getenv("AWS_SECRET_ACCESS_KEY")


@pytest.fixture
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.resource("s3", region_name=REGION_NAME)
