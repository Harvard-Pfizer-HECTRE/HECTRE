
from typing import Type

from .paper import Paper
from .parser import Parser

class PdfParser(Parser):
    '''
    This is the PDF parser class, and inherits from the base Parser class.
    This class has all the logic to take a file path or URL, get the contents,
    and parse it into a Paper object.
    '''

    @classmethod
    def from_file(cls, file_path: str) -> Type['PdfParser']:
        # TODO
        return cls(source=file_path)

    @classmethod
    def from_url(cls, url: str) -> Type['PdfParser']:
        # TODO
        return cls(source=url)
    
    def parse(self) -> Paper:
        # TODO
        raise NotImplementedError()
