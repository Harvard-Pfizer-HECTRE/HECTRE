import atexit
import io
import logging

import pdfplumber
import PyPDF2
from typing import Any, List, Optional
import urllib3

from hectre.input_parsers.parser import Parser
from hectre.pdf.page import Page
from hectre.pdf.paper import Paper
from hectre.pdf.table import Table


logger = logging.getLogger(__name__)


class PdfParserException(Exception):
    pass


class PdfParser(Parser):
    '''
    This is the PDF parser class, and inherits from the base Parser class.
    This class has the logic to take a file path or URL, and get the contents.
    '''
    file_path: Optional[str] = None
    url: Optional[str] = None
    llm: Optional[Any] = None

    file: Optional[Any] = None


    def __init__(self, file_path: Optional[str] = None, url: Optional[str] = None, llm: Optional[Any] = None):
        super().__init__()

        atexit.register(self.__cleanUp__)
        if url is not None:
            try:
                retry = urllib3.Retry(5)
                http = urllib3.PoolManager(retries=retry)
                self.file = io.BytesIO()
                self.file.write(http.request("GET", url).data)
            except Exception as e:
                logger.error(f"Could not open URL {url} for reading: {e}")
        elif file_path is not None:
            try:
                self.file = open(file_path, 'rb')
            except FileNotFoundError:
                logger.error(f"File not found: {file_path}")
        else:
            raise PdfParserException("Either file path or URL must be provided to PDF parser!")
        

    def __cleanUp__(self):
        if self.file is not None:
            self.file.close()


    def parse(self) -> Optional[Paper]:
        raise NotImplementedError()
