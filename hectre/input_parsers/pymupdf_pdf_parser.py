import logging

import fitz
from typing import List, Optional

from hectre.input_parsers.pdf_parser import PdfParser
from hectre.pdf.page import Page
from hectre.pdf.paper import Paper
from hectre.pdf.table import Table


logger = logging.getLogger(__name__)


class PdfParserException(Exception):
    pass


class PymupdfPdfParser(PdfParser):
    '''
    This parser uses PyMuPDF to detect tables and extract text.
    '''

    def parse(self) -> Optional[Paper]:
        pages: List[Page] = []
        tables: List[Table] = []

        plumber_path = self.file_path if self.file_path is not None else self.file

        pages_with_tables: int = 0

        doc = fitz.open(plumber_path)
        pageNum = 0
        for page in doc:
            pageNum += 1
            pageText = page.get_text()
            pageObj: Page = Page(number=pageNum, text=pageText)
            if len(page.find_tables().tables) > 1:
                print(pageNum)
                print(len(page.find_tables().tables))
                pages_with_tables += 1
                pageObj.set_has_table(True)
            pages.append(pageObj)
        logger.info(f"Parsed {pageNum} pages")
        extra_text = "" if pages_with_tables > 0 else ", using all pages for clinical data"
        logger.info(f"Done parsing, found {pages_with_tables} pages with tables{extra_text}")

        return Paper(pages=pages, tables=tables)
