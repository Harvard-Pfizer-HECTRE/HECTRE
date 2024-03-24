from typing import List

# Put any constants used by the tool here.
# Don't import any heavy dependencies, this file should be pure.

# Account related constants
AWS_PROFILE: str = "capstone"
AWS_REGION: str = "us-east-1"

# Logging constants
RESET: str = "\x1b[0m"
RED: str = "\x1b[31;20m"
BOLD_RED: str = "\x1b[31;1m"
GREEN: str = "\x1b[32;20m"
YELLOW: str = "\x1b[33;20m"
BLUE: str = "\x1b[34;20m"
PURPLE: str = "\x1b[35;20m"
CYAN: str = "\x1b[36;20m"
GREY: str = "\x1b[38;20m"
SILENCED_LOGGING_MODULES: List[str] = [
    "botocore",
    "urllib3",
]

# LLM related constants
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