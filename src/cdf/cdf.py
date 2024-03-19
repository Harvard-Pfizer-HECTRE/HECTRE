from pydantic import BaseModel
from typing import Optional

class Cdf(BaseModel):
    def __init__(self):
        # TODO
        # Each paper will have its own structure and row indexing.
        # Ex: paper ID 1 will have its own unique rows 1, 2, and 3;
        # and paper ID 2 will have its own unique rows 1, 2, and 3...
        # Then we consolidate them at the end.
        pass

    def set_value_for_paper_id(self, paper_id: int, col: int, value: str) -> None:
        '''
        We need to set some general values for a paper that will carry over to every
        single row. Ex: author names.
        '''
        if "," in value:
            # To be interchangeable with CSV, we cannot have commas in values.
            raise ValueError(f"Cannot accept commas in CDF cell. Column {col}, value: {value}")
        # TODO

    def set_value(self, paper_id: int, row: int, col: int, value: str) -> None:
        if "," in value:
            # To be interchangeable with CSV, we cannot have commas in values.
            raise ValueError(f"Cannot accept commas in CDF cell. Row {row}, column {col}, value: {value}")
        # TODO

    def get_value(self, paper_id: int, row: int, col: int) -> Optional[str]:
        # TODO
        pass