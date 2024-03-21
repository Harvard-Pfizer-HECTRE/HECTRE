from pydantic import BaseModel

class Table(BaseModel):
    '''
    This represents a table in a clinical trial paper.
    There are a method to fetch the contents of the table as plaintext,
    and a method to get the table number in the paper.
    '''
    number: int
    page_number: int
    text: str

    def get_number(self) -> int:
        '''
        Returns the number of this table. Indexed from zero.
        '''
        return self.number
    
    def get_page_number(self) -> int:
        '''
        Returns the page number where this table can be found. Indexed from zero.
        '''
        return self.page_number
    
    def get_text(self) -> str:
        '''
        Returns the contents of this table.
        '''
        return self.text