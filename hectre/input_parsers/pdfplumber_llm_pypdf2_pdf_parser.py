import logging

import pdfplumber
import PyPDF2
from typing import List, Optional

from hectre.input_parsers.pdf_parser import PdfParser
from hectre.pdf.page import Page
from hectre.pdf.paper import Paper
from hectre.pdf.table import Table


logger = logging.getLogger(__name__)


class PdfPlumberLlmPypdf2PdfParser(PdfParser):
    '''
    This parser uses PdfPlumber to detect tables,
    but use LLM as back-up if it cannot detect at least 2 pages with tables,
    and PyPdf2 to read text from pages.
    '''

    def parse(self) -> Optional[Paper]:
        pages: List[Page] = []
        tables: List[Table] = []

        plumber_path = self.file_path if self.file_path is not None else self.file

        pages_with_tables: int = 0

        try:
            with pdfplumber.open(plumber_path) as pdfplumber_file:
                pdf_file_reader = PyPDF2.PdfReader(self.file)
                # get the number of pages in the PDF
                num_pages = len(pdf_file_reader.pages)
                logger.info(f"Parsing {num_pages} pages...")

                # extract the text and tables of every page
                for page_index in range(num_pages):
                    logger.debug(f"Reading page {page_index + 1}")
                    pageObj = pdf_file_reader.pages[page_index]
                    # create Page object and append to list
                    page: Page = Page(number=page_index, text=pageObj.extract_text())

                    # Try to find tables if any
                    pdfplumber_page = pdfplumber_file.pages[page_index]
                    pdfplumber_tables = pdfplumber_page.find_tables(table_settings={})
                    if len(pdfplumber_tables) > 1:
                        logger.debug(f"Got table(s) on page {page_index + 1}")
                        pages_with_tables += 1
                        page.set_has_table(True)
                        
                    pages.append(page)

                # If we can't find more than 2 pages with tables, re-do with LLM
                if pages_with_tables < 3:
                    logger.info("Fall back to using LLM to detect tables")
                    pages_with_tables = 0
                    for page_index in range(num_pages):
                        page = pages[page_index]
                        page.set_has_table(False)
                        result = self.hectre.get_has_table_in_page(page)
                        if result:
                            logger.debug(f"Got table(s) on page {page_index + 1}")
                            pages_with_tables += 1
                            page.set_has_table(True)
        except Exception as e:
            logger.error(f"Got exception in PDF parsing: {e}")
            return None
        
        extra_text = "" if pages_with_tables > 0 else ", using all pages for clinical data"
        logger.info(f"Done parsing, found {pages_with_tables} pages with tables{extra_text}")

        return Paper(pages=pages, tables=tables)
