from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile, status, APIRouter
from loguru import logger
import magic
import os

KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}

router = APIRouter(
    prefix="/files",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

AWS_BUCKET = 'hectre-journals'

s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_BUCKET)

async def s3_upload(contents: bytes, key: str):
    logger.info(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)

async def s3_download(key: str):
    try:
        return s3.Object(bucket_name=AWS_BUCKET, key=key).get()['Body'].read()
    except ClientError as err:
        logger.error(str(err))

@router.get('/')
async def home():
    return {'message': 'Hello from file-upload 😄👋🏾'}


@router.post("/upload/")
async def upload(file: UploadFile):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file found!!'
        )

    contents = await file.read()
    size = len(contents)

    if not 0 < size <= 1 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supported file size is 0 - 1 MB'
        )

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
        )
    file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
    await s3_upload(contents=contents, key=file_name)
    return {'file_name': file_name}

@router.post("/upload_files/")
async def upload_files(files: list[UploadFile]):
    for file in files:
        # Generate a unique key for each file (e.g., using the original filename)
        key = os.path.join("uploads", file.filename)

        # Upload the file to S3
        bucket.put_object(Key=key, Body=file.file)
        # s3.upload_fileobj(file.file, AWS_BUCKET, key)

    return {"message": f"{len(files)} files uploaded successfully!"}