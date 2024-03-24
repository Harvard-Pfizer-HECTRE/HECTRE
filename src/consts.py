from typing import Dict, List

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
    # "DSID", # This is set by Pfizer, we don't care about this one
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
    "N.STUDY",
    "STATANAL.POP",
    "STATANAL.METHOD",
    # "STATANAL.IMP.METHOD", # We are not going to be imputing missing data
]

PER_TREATMENT_ARM_HEADERS: List[str] = [
    # "ARM.NUM", # All we need to do is hardcode placebo to be arm 0, then the others can be 1, 2, 3... in any order
    "ARM.BLIND", # Apparently the blindness can differ between treatment arms, cool
    "ARM.RANDFLG",
    "ARM.TRT",
    "ARM.TRTCLASS",
    "ARM.DOSE",
    "ARM.DOSEU",
    "ARM.ROUTE",
    "ARM.REGIMEN",
    "ARM.FORMULATION",
    "N.ARM",
    "ARM.TIME1",
    "ARM.TIME1U",
    "ARM.PCT.MALE",
    "ARM.AGE",
    "ARM.AGEU",
]

PER_TREATMENT_ARM_PER_TIME_HEADERS: List[str] = [
    "N.ARM.STATANAL", # Number of subjects at each treatment arm at each time
]

CLINICAL_DATA_HEADERS: List[str] = [
    "N.ARM.EVENT.SUBJ",
    # Baseline characteristics
    "BSL.STAT",
    "BSL.VAL",
    "BSL.VALU",
    "BSL.VAR",
    "BSL.VARU",
    "BSL.LCI",
    "BSL.UCI",
    # Change from baseline
    "CHBSL.STAT",
    "CHBSL.VAL",
    "CHBSL.VALU",
    "CHBSL.VAR",
    "CHBSL.VARU",
    "CHBSL.LCI",
    "CHBSL.UCI",
    # Response
    "RSP.STAT",
    "RSP.VAL",
    "RSP.VALU",
    "RSP.VAR",
    "RSP.VARU",
    "RSP.LCI",
    "RSP.UCI",
    # Percent change from baseline
    "PCHBSL.STAT",
    "PCHBSL.VAL",
    "PCHBSL.VAR",
    "PCHBSL.VARU",
    "PCHBSL.LCI",
    "PCHBSL.UCI",
]

SHORT_NAME_HEADER: str = "Field Name"
READABLE_NAME_HEADER: str = "Field Label"

# Prompting related constants
NO_DATA: str = "NO_DATA"

VAR_DICT: Dict[str, str] = {
    "Page_Start_Indicator": "[Page Begins]\n",
    "Page_End_Indicator": "\n[Page Ends]",
    "No_Data": NO_DATA,
}