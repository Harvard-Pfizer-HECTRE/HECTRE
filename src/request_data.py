from picos import Picos
from pprint import pprint

picos_reqs = [
    {
        'population': {
            'disease': 'T2D',
            'sub_populations': [
                    'cardiovascular disease',
                    'obese',
                    'chronic kidney disease',
                    'hypertension',
                    'hepatic steatosis',
                    'hypertriglyceridemia' 
            ]
        },
        'interventions': [
            {
                'drug_name': 'canagliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'empagliflozin',
                'drug_class': 'dapagliflozin'
            },
            {
                'drug_name': 'dapagliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'ertugliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'henagliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'ipragliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'luseogliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'remogliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'sotagliflozin',
                'drug_class': 'SGLT2'
            },
            {
                'drug_name': 'tofogliflozin',
                'drug_class': 'SGLT2'
            }
        ],
        'comparators': {
            'placebo',
            'active including standard of care'
        },
        'outcomes': {
            'body weight loss'
        },
        'study_designs': {
            'Parallel placebo controlled double blind',
            'single blind or triple blind studies'
        }
    }
]

if __name__ == '__main__':
    # Creates a fully validated Picos instance using the above test data
    # Dumps the pretty-printed JSON representation of the Picos instance.
    for p in picos_reqs:
        _p = Picos(**p)
        pprint(_p.model_dump(mode='json'))