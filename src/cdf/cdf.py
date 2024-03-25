"""A model for working with CDF data.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, TypeVar, Optional
import json
import pandas as pd
from pathlib import Path

# Relative to parent directory of this file.
FIELD_DEFINITIONS_FILENAME = "field_definitions.json"

FieldsBaseType = TypeVar('FieldsBaseType')
ClinicalType = TypeVar('ClinicalType')
LiteratureType = TypeVar('LiteratureType')

# Create fields dynamically for LiteratureData and Result models based on definitions.json
# Create method of CDF to create dataframe from LiteratureData and Results

class CDFData(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: field_name.replace('_', '.')
    )

class LiteratureData(CDFData):
    DSID: str = Field(default='')
    AU: str = Field(default='')
    TI: str = Field(default='')
    JR: str = Field(default='')
    PY: str = Field(default='')
    VL: str = Field(default='')
    IS: str = Field(default='')
    PG: str = Field(default='')
    AB: str = Field(default='')
    SA: str = Field(default='')
    REGID: str = Field(default='')
    STD_IND: str = Field(default='')
    STD_DESIGN: str = Field(default='')
    STD_GEO_LOCATION: str = Field(default='')
    STD_PHASE: str = Field(default='')


class ClinicalData(CDFData):
    ARM_NUM: str = Field(default='')
    ARM_BLIND: str = Field(default='')
    ARM_RANDFLG: str = Field(default='')
    ARM_TRT: str = Field(default='')
    ARM_TRTCLASS: str = Field(default='')
    ARM_DOSE: str = Field(default='')
    ARM_DOSEU: str = Field(default='')
    ARM_ROUTE: str = Field(default='')
    ARM_REGIMEN: str = Field(default='')
    ARM_FORMULATION: str = Field(default='')
    N_STUDY: str = Field(default='')
    N_ARM: str = Field(default='')
    N_ARM_STATANAL: str = Field(default='')
    N_ARM_EVENT_SUBJ: str = Field(default='')
    STATANAL_POP: str = Field(default='')
    STATANAL_METHOD: str = Field(default='')
    STATANAL_IMP_METHOD: str = Field(default='')
    ARM_TIME1: str = Field(default='')
    ARM_TIME1U: str = Field(default='')
    ENDPOINT: str = Field(default='')
    BSL_STAT: str = Field(default='')
    BSL_VAL: str = Field(default='')
    BSL_VALU: str = Field(default='')
    BSL_VAR: str = Field(default='')
    BSL_VARU: str = Field(default='')
    BSL_LCI: str = Field(default='')
    BSL_UCI: str = Field(default='')
    CHBSL_STAT: str = Field(default='')
    CHBSL_VAL: str = Field(default='')
    CHBSL_VALU: str = Field(default='')
    CHBSL_VAR: str = Field(default='')
    CHBSL_VARU: str = Field(default='')
    CHBSL_LCI: str = Field(default='')
    CHBSL_UCI: str = Field(default='')
    RSP_STAT: str = Field(default='')
    RSP_VAL: str = Field(default='')
    RSP_VALU: str = Field(default='')
    RSP_VAR: str = Field(default='')
    RSP_VARU: str = Field(default='')
    RSP_LCI: str = Field(default='')
    RSP_UCI: str = Field(default='')
    PCHBSL_STAT: str = Field(default='')
    PCHBSL_VAL: str = Field(default='')
    PCHBSL_VAR: str = Field(default='')
    PCHBSL_VARU: str = Field(default='')
    PCHBSL_LCI: str = Field(default='')
    PCHBSL_UCI: str = Field(default='')
    ARM_PCT_MALE: str = Field(default='')
    ARM_AGE: str = Field(default='')
    ARM_AGEU: str = Field(default='')


def get_field_defs() -> List[Dict]:
    working_directory = Path(__file__).absolute().parent
    path = working_directory / FIELD_DEFINITIONS_FILENAME
    with path.open() as f:
        fields = json.loads(f.read())
    return fields

def print_field_defs():
    field_defs = get_field_defs()
    for field in field_defs:
        fname = field['Field Name'].replace('.', '_')
        print(f'{fname}: str = Field(default='')')
class CDF(BaseModel):
    literature_data: Optional[LiteratureData] = None
    clinical_data: Optional[List[ClinicalData]] = []

    def set_literature_data(self, values: Dict) -> None:
        self.literature_data = LiteratureData(**values)
    
    def add_clinical_data(self, values: Dict) -> None:
        self.clinical_data.append(ClinicalData(**values))
    
    def to_df(self) -> pd.DataFrame:
        rows = []
        for result in self.clinical_data:
            row = self.literature_data.model_dump() | result.model_dump()
            rows.append(row)
        df = pd.DataFrame(rows)
        return df
