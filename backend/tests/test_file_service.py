import pytest
from services.files_service import FileS3Client
import boto3
import moto
from tests.test_aws_conf import *
from consts import TEST_S3_BUCKET

from fastapi.testclient import TestClient
from fastapi import UploadFile
from main import app


file_client = FileS3Client()
test_client = TestClient(app)


@pytest.fixture
def bucket_name():
    return TEST_S3_BUCKET


@pytest.fixture
def create_empty_bucket(s3_client, bucket_name):
    """Fixture to create an empty bucket for testing 😀"""
    with moto.mock_aws():
        s3 = boto3.resource("s3")
        yield s3.create_bucket(Bucket=bucket_name)


@pytest.fixture
def mock_files():
    return [mock_upload_file("test.txt1", "This is some test content.")]


def mock_upload_file(filename: str, content: str) -> UploadFile:
    return UploadFile(filename=filename, file=content.encode())


def test_created_bucket(s3_client, create_empty_bucket):
    """Fixture to confirm test bucket was created 😀"""
    buckets = file_client.list_buckets()
    assert buckets == [TEST_S3_BUCKET]


# Test upload_files
def test_upload_files(mock_files):
    """Test upload_files method 😀"""
    upload_success = file_client.upload_files(mock_files)
    assert upload_success == True
