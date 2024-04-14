import logging
import time

from fastapi import UploadFile, status, APIRouter
from loguru import logger

from typing import List
from multiprocessing.pool import ThreadPool
from backend.services.files_service import FileS3Client
from backend.utils.response_handler import ResponseHandler
from backend.utils.service_result import handle_result
from backend.consts import REGION_NAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/files",
    tags=["Uploads"],
    responses={404: {"description": "Not found"}},
)

files_client = FileS3Client(region_name=REGION_NAME)


@router.post("/upload_files/")
async def upload_files(files: List[UploadFile]):
    upload_success = files_client.upload_files_to_s3(files)

    return ResponseHandler.handle_upload_response(upload_success)
