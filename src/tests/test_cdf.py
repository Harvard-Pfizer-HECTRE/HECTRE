from ..cdf.cdf import *

'''
This file is used to run unit tests for the CDF module.
'''

def test_from_json():
    lit = LiteratureData(**{"AU": "JFN:MM"})
    c1 = '{"BSL.LCI": 8.7}'
    c2 = '{"CHBSL.VARU": "SD"}'
    clin = ClinicalData.from_json(c1, c2)
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    df = cdf.to_df()
    actual_numrows = df.shape[0]
    expected_numrows = 2
    assert actual_numrows == expected_numrows