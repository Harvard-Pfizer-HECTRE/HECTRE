
from pydantic import BaseModel
from typing import Any

class Parser(BaseModel):
    '''
    This is the base class for a generic parser. It should be able to be
    instantiated either from a file path or an URL.

    This class is abstract, and we need to implement specific parser classes on top of it.
    '''
    def parse(self) -> Any:
        raise NotImplementedError("Calling parse() on abstract class Parser.")
