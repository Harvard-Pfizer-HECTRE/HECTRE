"""A module for working with PICOS data.

This module defines a PICOS type and associate sub-types that will be used to
validate user provided PICOS data.
"""
from typing import List
from pydantic import BaseModel

class Intervention(BaseModel):
    """Represents an Intervention, or the "I" in PICOS.

    Attributes:
        name: The primary name of the intervention.
        synonyms: Other names names used to refer to this intervention.
    """
    name: str
    synonyms: List[str]

class Outcome(BaseModel):
    """Represents an Outcome, or the "O" in PICOS.

    Attributes:
        name: The primary name of the intervention.
        synonyms: Other names names used to refer to this Outcome.
    """
    name: str
    synonyms: List[str]

class Picos(BaseModel):
    """Represents a PICOS object used during a systematic review.

    Attributes:
        population: The patient population.
        intervention: The treatments being considered.
        comparitors: The main alternative to the intervention.
        outcomes: What is being measured.
        study_design: The type of studies being considered.
    """
    population: str
    interventions: List[Intervention]
    comparitors: str
    outcomes: List[Outcome]
    study_design: str