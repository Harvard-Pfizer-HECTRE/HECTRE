from pydantic import BaseModel

class Page(BaseModel):
    def __init__(self):
        # TODO
        pass

    def get_number(self) -> int:
        '''
        Returns the number of this page.
        '''
        # TODO
        raise NotImplementedError()
    
    def get_text(self) -> str:
        '''
        Returns the contents of this page.
        '''
        # TODO
        raise NotImplementedError()