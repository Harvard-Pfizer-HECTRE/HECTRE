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
    This class has all the logic to take a file path or URL, get the contents,
    and parse it into a Paper object.
    '''
    file_path: Optional[str] = None
    url: Optional[str] = None
    file: Optional[Any] = None


    def __init__(self, file_path: str = None, url: str = None):
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
        pages: List[Page] = []
        tables: List[Table] = []

        plumber_path = self.file_path if self.file_path is not None else self.file

        try:
            with pdfplumber.open(plumber_path) as pdfplumber_file:
                pdf_file_reader = PyPDF2.PdfReader(self.file)
                # get the number of pages in the PDF
                num_pages = len(pdf_file_reader.pages)
                logger.info(f"Found {num_pages} pages in the PDF")

                # extract the text and tables of every page
                for page_index in range(num_pages):
                    logger.info(f"Reading page {page_index + 1}")
                    pageObj = pdf_file_reader.pages[page_index]
                    # create Page object and append to list
                    page: Page = Page(number=page_index, text=pageObj.extract_text())
                    pages.append(page)

                    # Try to find tables if any
                    pdfplumber_page = pdfplumber_file.pages[page_index]
                    pdfplumber_tables = pdfplumber_page.find_tables(table_settings={})
                    if len(pdfplumber_tables) > 1:
                        logger.info(f"Got table(s) on page {page_index + 1}")
                        page.set_has_table(True)
        except Exception as e:
            logger.error(f"Got exception in PDF parsing: {e}")
            return None

        return Paper(pages=pages, tables=tables)
