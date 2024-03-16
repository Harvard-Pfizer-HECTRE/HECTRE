from pydantic import BaseModel

class Table(BaseModel):
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