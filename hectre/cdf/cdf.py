"""A model for working with CDF data.
"""
from __future__ import annotations

from collections import OrderedDict
import os

from pydantic import BaseModel, Json
from typing import Any, List, Dict, Optional
import json
import pandas as pd
import warnings

from hectre.consts import (
    HEADER_ORDER,
    NO_DATA,
    CDF_COMPARE_COLS_IGNORE,
    CDF_COMPOUND_KEY_COLS,
    LITERATURE_DATA_HEADERS
    )

# Create fields dynamically for LiteratureData and Result models based on definitions.json
# Create method of CDF to create dataframe from LiteratureData and Results

class CDFData(BaseModel, extra='allow'):
    def __init__(self, **kwargs):
        super().__init__()
        for key, val in kwargs.items():
            setattr(self, key, val)


    @classmethod
    def from_dict(cls, values: Dict) -> CDFData:
        return cls(**values)
    

    @classmethod
    def from_dicts(cls, *dicts: Dict[str, Any]) -> CDFData:
        values = OrderedDict()
        for header in HEADER_ORDER:
            for dictionary in dicts:
                if header in dictionary:
                    values[header] = dictionary[header] if NO_DATA not in str(dictionary[header]) else ""
                    break
            if header not in values:
                values[header] = ""
        return cls(**values)


    @classmethod
    def from_json(cls, *json_strs: Json[Dict]) -> CDFData:
        values = {}
        for json_str in json_strs:
            deserialized = json.loads(json_str)
            values.update(deserialized)
        return cls.from_dict(values)
    

class CDF(BaseModel):
    literature_data: Optional[CDFData] = None
    clinical_data: List[CDFData] = []


    def set_literature_data(self, values: CDFData) -> None:
        self.literature_data = values

    
    def add_clinical_data(self, values: CDFData) -> None:
        self.clinical_data.append(values)

    
    def to_df(self) -> pd.DataFrame:
        rows = []
        for result in self.clinical_data:
            row = result.model_dump()
            for key, val in self.literature_data.model_dump().items():
                if str(val) and NO_DATA not in str(val):
                    row[key] = val
            rows.append(row)
        df = pd.DataFrame(rows)
        return df
    

    def save_to_string(self) -> str:
        # Return the full CSV string
        return self.to_df().to_csv(index=False)
    

    def save_to_file(self, name, path=os.path.join(os.path.dirname(__file__), "../../output")) -> None:
        # Save the CDF contents to file
        if not os.path.exists(path):
            os.makedirs(path)
        self.to_df().to_csv(index=False, path_or_buf=os.path.join(path, f"{name}.csv"))

    def compare(self, test_cdf: pd.DataFrame, control_cdf: pd.DataFrame):
        # Suppress performance warning, our volume is low so this will not affect us.
        warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
        ck_cols = CDF_COMPOUND_KEY_COLS
        ex_cols = CDF_COMPARE_COLS_IGNORE
        # Make sure they have the same columns.
        cols_eq = set(test_cdf.columns) == set(control_cdf.columns)
        if not cols_eq:
            raise RuntimeError('The columns in the test and control CDFs are not the same')
        test_lit_data = test_cdf.loc[0,LITERATURE_DATA_HEADERS]
        test_clin_data = test_cdf.drop(columns=LITERATURE_DATA_HEADERS)
        test_clin_data.set_index(ck_cols,inplace=True)
        # Confrol CDF (considered 100% accurate)
        control_lit_data = control_cdf.loc[0,LITERATURE_DATA_HEADERS]
        control_clin_data = control_cdf.drop(columns=LITERATURE_DATA_HEADERS)
        control_clin_data.set_index(ck_cols,inplace=True)
        clin_results = self.compare_clinical_data(test_clin_data, control_clin_data)
        results = {
            "test_clin_data": test_clin_data,
            "test_lit_data": test_lit_data,
            "control_clin_data": control_clin_data,
            "control_lit_data": control_lit_data,
            "comp_summary": clin_results['comp_summary'],
            "comp_eq_matrix": clin_results['comp_equality_matrix']
        }
        return results
    
    def compare_clinical_data(self, test_df: pd.DataFrame, control_df: pd.DataFrame):
        # Create a DataFrame to hold comparison summary.
        comp_summary = pd.DataFrame(columns=['Exists in Control', 'Equals Control', 'Unique in Test', 'Unique in Control'], index=test_df.index)
        # Create a DataFrame to hold cell-by-cell equality matrix.
        eq_df = pd.DataFrame(columns=test_df.columns, index=test_df.index)
        for i_test_df, row in test_df.iterrows():
            control_rows = control_df[control_df.index.isin([i_test_df])]
            test_rows = test_df[test_df.index.isin([i_test_df])]
            row_results = {
                'Exists in Control': False,
                'Equals Control': False,
                'Unique in Test': False,
                'Unique in Control': False
            }
            if not control_rows.empty:
                row_results['Exists in Control'] = True
                if control_rows.shape[0] == 1:
                    row_results['Unique in Control'] = True
                for index_s, val in control_rows.iloc[0].items():
                    eq_df.loc[i_test_df, index_s] = (val == row[index_s])
                row_results['Equals Control'] = eq_df.loc[i_test_df].all()
            if test_rows.shape[0] == 1:
                row_results['Unique in Test'] = True
            comp_summary.loc[i_test_df] = row_results
        results = {
            'comp_equality_matrix': eq_df,
            'comp_summary': comp_summary
        }
        return results



