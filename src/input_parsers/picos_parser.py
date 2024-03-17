
from typing import Type

from .parser import Parser
from .picos import Picos

class PicosParser(Parser):
    '''
    This is the PICOS parser class, and inherits from the base Parser class.
    This class has all the logic to take a string and parse it into a Picos object.
    '''

    def __init__(self, source: str, **kwargs):
        super().__init__()
        # TODO
        pass
    
    def parse(self) -> Picos:
        # TODO
        raise NotImplementedError()
