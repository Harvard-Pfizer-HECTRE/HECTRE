from pydantic import BaseModel

class Page(BaseModel):
    '''
    This is the implementation of a page in a clinical trial paper.
    We should be able to get the contents, as well as the page number from this object.
    '''
    number: int
    text: str

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