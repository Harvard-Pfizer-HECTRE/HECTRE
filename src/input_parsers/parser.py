
from pydantic import BaseModel
from typing import Type

from .paper import Paper

class Parser(BaseModel):
    '''
    This is the base class for a generic parser. It should be able to be
    instantiated either from a file path or an URL.

    This class is abstract, and we need to implement specific parser classes on top of it.
    '''

    def __init__(self, source: str, **kwargs):
        self.source = source

    @classmethod
    def from_file(cls, file_path: str) -> Type['Parser']:
        return cls(file_path)

    @classmethod
    def from_url(cls, url: str) -> Type['Parser']:
        return cls(url)
    
    def parse(self) -> Paper:
        raise NotImplementedError("Calling parse() on abstract class Parser.")
