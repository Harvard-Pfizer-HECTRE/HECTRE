import logging
import time

from fastapi import UploadFile, status, APIRouter, Response
from loguru import logger

from typing import List
from multiprocessing.pool import ThreadPool
from backend.services.files_service import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


router = APIRouter(
    prefix="/files",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload_files/")
async def upload_files(files: List[UploadFile]):

    pool = ThreadPool(len(files))
    
    startime = time.time()
    results = pool.map(upload_file, files)
    endtime = time.time() - startime

    pool.close()

    if all(results):
        logger.debug(f"all {len(files)} files uploaded in : {endtime} seconds")
        
        message = "All files uploaded successfully!"
        response = Response(content=message, status_code=status.HTTP_200_OK)
        
        # invoke hectre api here

        return response
    else:
        message = "Files failed to upload!"
        logger.error(f"{message}")
        response = Response(content=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response