"""A module for working with PICOS data.

This module defines a PICOS type and associate sub-types that will be used to
validate user provided PICOS data.
"""
from typing import Set
from pydantic import BaseModel

class PicosAliased(BaseModel):
    """Base class for a PICOS aliased type.

    Attributes:
        names: Names used to refer to this item.
    """
    names: Set[str]

class Population(PicosAliased):
    """Represents an Population, or the "P" in PICOS.
    """

class Intervention(PicosAliased):
    """Represents an Intervention, or the "I" in PICOS.
    """

class Comparator(PicosAliased):
    """Represents a Comparator, or the "C" in PICOS.
    """

class Outcome(PicosAliased):
    """Represents an Outcome, or the "O" in PICOS.
    """

class Study_Design(PicosAliased):
    """Represents a Study Design, or the "S" in PICOS.
    """

class Picos(BaseModel):
    """Represents a PICOS object used during a systematic review.

    Attributes:
        populations: The patient populations.
        interventions: The treatments being considered.
        comparitors: The alternatives to the interventions.
        outcomes: What is being measured.
        study_designs: The type of studies being considered.
    """
    populations: Set[Population]
    interventions: Set[Intervention]
    comparators: Set[Comparator]
    outcomes: Set[Outcome]
    study_designs: Set[Study_Design]