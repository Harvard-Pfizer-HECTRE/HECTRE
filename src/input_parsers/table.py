from pydantic import BaseModel

class Table(BaseModel):
    '''
    This represents a table in a clinical trial paper.
    There are a method to fetch the contents of the table as plaintext,
    and a method to get the table number in the paper.
    '''

    def __init__(self):
        # TODO
        pass

    def get_number(self) -> int:
        '''
        Returns the number of this table.
        '''
        # TODO
        raise NotImplementedError()
    
    def get_text(self) -> str:
        '''
        Returns the contents of this table.
        '''
        # TODO
        raise NotImplementedError()