from pydantic import BaseModel

from ..consts import UNICODE_REPLACE_MAP

class Page(BaseModel):
    '''
    This is the implementation of a page in a clinical trial paper.
    We should be able to get the contents, as well as the page number from this object.
    '''
    number: int
    text: str
    has_table: bool = False

    def __init__(self, number: int, text: str, has_table: bool = False) -> None:
        super().__init__(number=number, text=text, has_table=has_table)

        # Replace some of the unicode text
        for unicode, replacement in UNICODE_REPLACE_MAP.items():
            text = text.replace(unicode, replacement)

        self.text = text


    def get_number(self) -> int:
        '''
        Returns the number of this page. Indexed from zero.
        '''
        return self.number
    

    def get_text(self) -> str:
        '''
        Returns the contents of this page.
        '''
        return self.text
    

    def set_has_table(self, has_table: bool) -> None:
        '''
        Sets whether this page has a table.
        '''
        self.has_table = has_table


    def get_has_table(self) -> bool:
        '''
        Returns whether this page has a table.
        '''
        return self.has_table
