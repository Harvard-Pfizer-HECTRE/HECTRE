import logging

from pydantic import BaseModel
from typing import Optional, Set

from hectre.consts import (
    ALLOWED_UNICODE_CHARS,
    UNICODE_REPLACE_MAP
)

logger = logging.getLogger(__name__)


class Page(BaseModel):
    '''
    This is the implementation of a page in a clinical trial paper.
    We should be able to get the contents, as well as the page number from this object.
    '''
    number: int
    text: str
    has_table: bool = False
    unknown_unicode_chars: Optional[Set[str]] = None


    def __init__(self, number: int, text: str, has_table: bool = False, unknown_unicode_chars: Optional[Set[str]] = None) -> None:
        super().__init__(number=number, text=text, has_table=has_table, unknown_unicode_chars=unknown_unicode_chars)
        self.unknown_unicode_chars = set()

        # Replace some of the unicode text
        for unicode, replacement in UNICODE_REPLACE_MAP.items():
            text = text.replace(unicode, replacement)

        # Warn on any unknown unicode characters
        for char in text:
            if ord(char) > 127 and char not in ALLOWED_UNICODE_CHARS:
                logger.debug(f"Detected unknown unicode character: {char}")
                self.unknown_unicode_chars.add(char)

        self.text = text


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
    

    def set_has_table(self, has_table: bool) -> None:
        '''
        Sets whether this page has a table.
        '''
        self.has_table = has_table


    def get_has_table(self) -> bool:
        '''
        Returns whether this page has a table.
        '''
        return self.has_table
