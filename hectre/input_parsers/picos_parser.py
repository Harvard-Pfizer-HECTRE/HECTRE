
from hectre.input_parsers.parser import Parser
from hectre.picos.picos import (
    Picos,
    Population,
)


class PicosParser(Parser):
    '''
    This is the PICOS parser class, and inherits from the base Parser class.
    This class has all the logic to take a string and parse it into a Picos object.
    '''
    picos_string: str

    def parse(self) -> Picos:
        # Simple parser that expects the picos string to just be semi-colon-separated outcomes
        outcomes = self.picos_string.split(";")
        return Picos(population=Population(disease="", sub_populations=set()), interventions=set(), comparators=set(), outcomes=set(outcomes), study_designs=set())
