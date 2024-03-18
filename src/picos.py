"""A module for working with PICOS data.

This module defines a PICOS type and associate sub-types that will be used to
validate user provided PICOS data.
"""
from typing import Set
from pydantic import BaseModel

class Population(BaseModel):
    """Represents a Population, or the "P" in PICOS.
    """
    disease: str
    sub_populations: Set[str]

class Intervention(BaseModel):
    """Represents an Intervention, or the "I" in PICOS.
    """
    drug_name: str
    drug_class: str
    def __hash__(self):
        return hash((self.drug_name, self.drug_class))
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.drug_name == other.drug_name and
            self.drug_class == other.drug_class
        )

class Picos(BaseModel):
    """Represents a PICOS object used during a systematic review.

    Attributes:
        populations: The patient populations.
        interventions: The treatments being considered.
        comparitors: The alternatives to the interventions.
        outcomes: What is being measured.
        study_designs: The type of studies being considered.
    """
    population: Population
    interventions: Set[Intervention]
    comparators: Set[str]
    outcomes: Set[str]
    study_designs: Set[str]