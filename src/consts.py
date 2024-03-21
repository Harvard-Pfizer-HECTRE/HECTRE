from typing import List

# Put any constants used by the tool here.
# Don't import any heavy dependencies, this file should be pure.

AWS_PROFILE: str = "capstone"
AWS_REGION = "us-east-1"

LITERATURE_DATA_HEADERS: List[str] = [
    "DSID",
    "AU",
    "TI",
    "JR",
    "PY",
    "VL",
    "IS",
    "PG",
    "AB",
    "SA",
    "REGID",
    "STD.IND",
    "STD.DESIGN",
    "STD.GEO.LOCATION",
    "STD.PHASE",
]

SKIPPED_LITERATURE_DATA_HEADERS: List[str] = [
    "DSID",
]

SHORT_NAME_HEADER = "Field Name"
READABLE_NAME_HEADER = "Field Label"
FIELD_DESCRIPTION_HEADER = "Field Description"

NO_DATA = "NO_DATA"