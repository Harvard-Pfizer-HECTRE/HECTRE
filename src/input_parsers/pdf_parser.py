import logging
from typing import Any, List, Optional

import PyPDF2
import tabula

from .page import Page
from .paper import Paper
from .parser import Parser
from .table import Table


logger = logging.getLogger(__name__)


class PdfParserException(Exception):
    pass


class PdfParser(Parser, extra='allow'):
    '''
    This is the PDF parser class, and inherits from the base Parser class.
    This class has all the logic to take a file path or URL, get the contents,
    and parse it into a Paper object.
    '''
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

                    # try extracting any tables
                    try:
                        tabula_tables = tabula.read_pdf(self.file_path, pages=page_index + 1, silent=True)

                        for i in range(0, len(tabula_tables)):
                            logger.info(f"Reading table {table_number} on page {page_index + 1}")
                            # get rid of indexes
                            table_no_ind = tabula_tables[i].set_index(tabula_tables[i].columns[0])
                            # create Table object and append to list
                            table: Table = Table(number=table_number, page_number=page_index, text=table_no_ind.to_string())
                            tables.append(table)
                            table_number += 1
                    except UnicodeDecodeError:
                        pass
        # if there is no file with this name - throw an error
        except FileNotFoundError:
            raise PdfParserException(f"File not found: {self.file_path}")
        
        return Paper(pages=pages, tables=tables)
    