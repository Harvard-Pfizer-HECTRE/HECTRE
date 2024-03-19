
from .parser import Parser
from .picos import Picos

class PicosParser(Parser):
    '''
    This is the PICOS parser class, and inherits from the base Parser class.
    This class has all the logic to take a string and parse it into a Picos object.
    '''
    picos_string: str

    def parse(self) -> Picos:
        # TODO
        raise NotImplementedError()
