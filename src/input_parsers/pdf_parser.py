import logging
from typing import List

import pdfplumber
import PyPDF2

from ..pdf.page import Page
from ..pdf.paper import Paper
from .parser import Parser
from ..pdf.table import Table


logger = logging.getLogger(__name__)


class PdfParserException(Exception):
    pass


class PdfParser(Parser):
    '''
    This is the PDF parser class, and inherits from the base Parser class.
    This class has all the logic to take a file path or URL, get the contents,
    and parse it into a Paper object.
    '''
    file_path: str = None

    def __init__(self, file_path: str = None, url: str = None):
        super().__init__()

        if file_path is None and url is None:
            raise PdfParserException("Either file path or URL must be provided to PDF parser!")

        if url is not None:
            raise NotImplementedError()

        self.file_path = file_path


    def parse(self) -> Paper:
        pages: List[Page] = []
        tables: List[Table] = []

        try:
            with open(self.file_path, 'rb') as file:
                with pdfplumber.open(self.file_path) as pdfplumber_file:
                    pdf_file_reader = PyPDF2.PdfFileReader(file)
                    # get the number of pages in the PDF
                    num_pages = pdf_file_reader.numPages
                    logger.info(f"Found {num_pages} pages in the PDF")

                    table_number = 1
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

        # if there is no file with this name - throw an error
        except FileNotFoundError:
            raise PdfParserException(f"File not found: {self.file_path}")

        return Paper(pages=pages, tables=tables)
