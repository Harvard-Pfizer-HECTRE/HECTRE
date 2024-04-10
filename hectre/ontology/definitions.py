import json
import os

from pydantic import BaseModel
from typing import Any, Dict

from hectre.consts import (
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


    def get_field_by_name(self, name: str) -> Dict[str, str]:
        '''
        Get the dictionary for this field by its short name.
        '''
        if name not in self.definitions_dict_by_short_name:
            raise DefinitionsException(f"Field name of {name} not found in definitions!")
        return self.definitions_dict_by_short_name[name]


    def get_field_by_label(self, name: str) -> Dict[str, str]:
        '''
        Get the dictionary for this field by its label (readable name).
        '''
        if name not in self.definitions_dict_by_readable_name:
            raise DefinitionsException(f"Field label of {name} not found in definitions!")
        return self.definitions_dict_by_readable_name[name]