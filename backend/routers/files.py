import logging
import time

from fastapi import UploadFile, File, APIRouter
from loguru import logger

from typing import List
from backend.services.files_service import FileS3Client
from backend.utils.response_handler import ResponseHandler
from backend.consts import REGION_NAME, S3_FOLDER_INPUT
from backend.models.extraction_request import ExtractionRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/files",
    tags=["Uploads"],
    responses={404: {"description": "Not found"}},
)

files_client = FileS3Client(region_name=REGION_NAME)


@router.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    upload_success = files_client.upload_file(file, folder=S3_FOLDER_INPUT)

    return ResponseHandler.handle_upload_response(upload_success)


@router.post("/upload_files/")
async def upload_files(files: List[UploadFile]):
    upload_success = files_client.upload_files(files)

    return ResponseHandler.handle_upload_response(upload_success)


@router.post("/extract/")
async def extract(request: ExtractionRequest):

    print(
        f"Extracting files from folder_id: {request.folder_id} with outcomes: {request.outcomes_string}"
    )
    await files_client.download_and_extract_files(
        request.folder_id, request.outcomes_string
    )

    return ResponseHandler.handle_extraction_response(True)
