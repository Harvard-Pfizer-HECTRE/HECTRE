"""A model for working with CDF data.
"""
from pydantic import BaseModel, create_model, Field
from typing import List, Dict, TypeVar, Generic, Type
import json
from pathlib import Path

# Relative to parent directory of this file.
FIELD_DEFINITIONS_FILENAME = "field_definitions.json"

FieldsBaseType = TypeVar('FieldsBaseType')
ClinicalType = TypeVar('ClinicalType')
LiteratureType = TypeVar('LiteratureType')

# Create fields dynamically for LiteratureData and Result models based on definitions.json
# Create method of CDF to create dataframe from LiteratureData and Results

class FieldsBaseModel(BaseModel):
    pass

def create_fields_model(name: str, fields: List[Dict]):
    model_fields = {item['Field Name']: (str, '') for item in fields}
    model = create_model(
        name,
        __base__ = FieldsBaseModel,
        **model_fields
    )
    return model

def get_field_defs() -> List[Dict]:
    working_directory = Path(__file__).absolute().parent
    path = working_directory / FIELD_DEFINITIONS_FILENAME
    with path.open() as f:
        fields = json.loads(f.read())
    return fields

class CDF(BaseModel):
    field_defs: List[Dict]
    literature_field_defs: List[Dict]
    clinical_field_defs: List[Dict]
    literature_data: Dict
    clinical_data: List[Dict]

    @classmethod
    def create(cls):
        field_defs = get_field_defs()
        return cls(
            field_defs = field_defs,
            literature_field_defs = [field for field in field_defs if field['Category'] == 'Literature'],
            clinical_field_defs = [field for field in field_defs if field['Category'] == 'Clinical'],
            literature_data = {},
            clinical_data = []
        )
