from pydantic import BaseModel

from .page import Page
from .table import Table

class Paper(BaseModel):
    def __init__(self):
        # TODO
        pass

    def get_id(self) -> int:
        # Return some unique ID for this paper.
        raise NotImplementedError()

    def get_num_pages(self) -> int:
        # TODO
        raise NotImplementedError()

    def get_page(self, page_num: int) -> Page:
        # TODO
        raise NotImplementedError()

    def get_num_tables(self) -> int:
        # TODO
        raise NotImplementedError()

    def get_table(self, table_num: int) -> Table:
        # TODO
        raise NotImplementedError()