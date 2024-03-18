from typing import List

# Put any constants used by the tool here.
# Don't import any heavy dependencies, this file should be pure.

AWS_PROFILE: str = "capstone"
AWS_REGION = "us-east-1"

LITERATURE_DATA_HEADERS: List[str] = [
    # "DSID",
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