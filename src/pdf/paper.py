from pydantic import BaseModel
from typing import List

from ..consts import (
    PAGE_END_INDICATOR,
    PAGE_START_INDICATOR,
)
from .page import Page
from .table import Table

class Paper(BaseModel):
    '''
    This is the class for the clinical trial paper that has been parsed by the PDF parser.
    Each paper should have an unique ID, and methods to:
    - get total number of pages in this paper
    - get a specific page in this paper
    - get total number of tables in this paper
    - get a specific table in this paper

    Paper objects are instantiated by the PDF parser, and are used by the data extractor.
    '''
    pages: List[Page]
    tables: List[Table]

    def get_id(self) -> int:
        '''
        Each paper needs a unique ID to identify itself.
        This function returns that unique identifier.
        '''
        # TODO
        return 0

    def get_num_pages(self) -> int:
        '''
        Get the total number of pages in this paper.
        '''
        return len(self.pages)

    def get_page(self, page_num: int) -> Page:
        '''
        Get a specific page in this paper.
        '''
        return self.pages[page_num]

    def get_num_tables(self) -> int:
        '''
        Get the total number of tables in this paper.
        '''
        return len(self.tables)

    def get_table(self, table_num: int) -> Table:
        '''
        Get a specific table in this paper.
        '''
        return self.tables[table_num]
    

    def get_all_text(self) -> str:
        '''
        Get all text from the paper.
        '''
        ret = ""
        for page_num in range(self.get_num_pages()):
            page: Page = self.get_page(page_num)
            text = page.get_text()
            ret += PAGE_START_INDICATOR.format(page_num + 1)
            ret += text
            ret += PAGE_END_INDICATOR.format(page_num + 1)
        return ret