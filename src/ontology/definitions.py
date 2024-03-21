import json
import os

from pydantic import BaseModel
from typing import Any, Dict

from ..consts import (
    FIELD_DESCRIPTION_HEADER,
    READABLE_NAME_HEADER,
    SHORT_NAME_HEADER,
)


class DefinitionsException(Exception):
    pass


class Definitions(BaseModel):
    '''
    This class is used to convert shortened field names to readable names, or vice versa.
    '''
    definitions_path: str = None
    definitions_dict_by_short_name: Dict[str, Any] = None
    definitions_dict_by_readable_name: Dict[str, Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.definitions_path = os.path.join(os.path.dirname(__file__), "../../definitions.json")
        self.definitions_dict_by_short_name = {}
        self.definitions_dict_by_readable_name = {}
        
        with open(self.definitions_path, 'r') as jsonfile:
            data = json.load(jsonfile)
            for entry in data:
                short_name = entry[SHORT_NAME_HEADER]
                readable_name = entry[READABLE_NAME_HEADER]
                self.definitions_dict_by_short_name[short_name] = entry
                self.definitions_dict_by_readable_name[readable_name] = entry


    def convert_to_readable_name(self, short_name: str) -> str:
        '''
        Convert a shortened name, like IS or PG, to readable names like Publication Issue or Publication Pages.
        '''
        if short_name not in self.definitions_dict_by_short_name:
            raise DefinitionsException(f"Short name of {short_name} not found in definitions!")
        return self.definitions_dict_by_short_name[short_name][READABLE_NAME_HEADER]


    def convert_to_short_name(self, name: str) -> str:
        '''
        Convert a name, like Publication Issue or Publication Pages, to shortened names like IS or PG.
        '''
        if name not in self.definitions_dict_by_readable_name:
            raise DefinitionsException(f"Readable name of {name} not found in definitions!")
        return self.definitions_dict_by_readable_name[name][SHORT_NAME_HEADER]
    
    def get_field_description(self, short_name: str) -> str:
        '''
        Get a description of this field.
        '''
        if short_name not in self.definitions_dict_by_short_name:
            raise DefinitionsException(f"Short name of {short_name} not found in definitions!")
        return self.definitions_dict_by_short_name[short_name][FIELD_DESCRIPTION_HEADER]