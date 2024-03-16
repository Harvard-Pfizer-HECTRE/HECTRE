
from typing import Type

from .paper import Paper
from .parser import Parser

class PdfParser(Parser):
    def __init__(self, source, **kwargs):
        super().__init__()
        # TODO
        pass

    @classmethod
    def from_file(cls, file_path: str) -> Type['PdfParser']:
        # TODO
        return cls(file_path)

    @classmethod
    def from_url(cls, url: str) -> Type['PdfParser']:
        # TODO
        return cls(url)
    
    def parse(self) -> Paper:
        # TODO
        raise NotImplementedError()
