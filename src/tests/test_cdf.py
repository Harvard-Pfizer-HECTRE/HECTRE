from cdf.cdf import *

'''
This file is used to run unit tests for the CDF module.
'''

def literature_data_should_equal_value_set_in_constructor():
    lit = LiteratureData(**{"AU": "JFN"})
    cdf = CDF()
    cdf.literature_data = lit
    assert cdf.literature_data.AU == 'JFN'

def clinical_data_should_equal_value_set_using_from_json():
    c1 = '{"BSL.LCI": 8.7}'
    c2 = '{"CHBSL.VARU": "SD"}'
    clin = ClinicalData.from_json(c1, c2)
    cdf = CDF()
    cdf.clinical_data = [clin]
    assert cdf.clinical_data[0].BSL_LCI == '8.7'