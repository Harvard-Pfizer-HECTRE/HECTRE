
from pydantic import BaseModel
from typing import Type

from .paper import Paper

class Parser(BaseModel):
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
