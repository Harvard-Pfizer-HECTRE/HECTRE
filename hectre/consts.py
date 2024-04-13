from typing import Dict, List

# Put any constants used by the tool here.
# Don't import any heavy dependencies, this file should be pure.

# ------------------------------
# Account related constants
# ------------------------------
AWS_PROFILE: str = "capstone"
AWS_REGION: str = "us-east-1"


# ------------------------------
# Logging constants
# ------------------------------
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
    "pdfminer",
]

LLM_BEGIN_PROMPT_LOGGING_INDICATOR = "BEGIN PROMPT\n"
LLM_END_PROMPT_LOGGING_INDICATOR = "\nEND PROMPT"
LLM_BEGIN_RESPONSE_LOGGING_INDICATOR = "BEGIN RESPONSE\n"
LLM_END_RESPONSE_LOGGING_INDICATOR = "\nEND RESPONSE"


# ------------------------------
# Extraction related constants
# ------------------------------
ALLOWED_UNICODE_CHARS: List[str] = [
    "©",
    "®",
    "™",
    # Operators
    "≤",
    "≥",
    "±",
    "Δ",
    # Some footnote denoters
    "†",
    "‡",
    "§",
    "¶",
    "⋅",
    "•", # These should be used for bullet points ONLY
    "●", # Not sure about this one... it was used as a divider
    # Some accented characters
    "á",
    "à",
    "ä",
    "ß",
    "é",
    "É",
    "ç",
    "ï",
    "í",
    "Ł",
    "ñ",
    "Ö",
    "ó",
    "ö",
    "Ø",
    "ø",
    "ü",
    # Math characters
    "Φ",
    "β",
    "μ",
    "π",
    "λ",
    "¼",
    "°",
]

UNICODE_REPLACE_MAP: Dict[str, str] = {
    # Should always replace
    u'\xa0': "",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "–": "-",
    "—": "-",
    "−": "-",
    "‑": "-",
    "‐": "-",  # Yes these five all all dashes
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
    "·": ".",
    "∗": "*",
    "ª": "©",
    "∆": "Δ",
    "∼": "~",
    "α": "a",
    "µ": "μ",
    "×": "x",
    "γ": "y",
    # May depend on paper
    " €a": "ä",
    "c ¸": "ç",
    " ´e": "é",
    " €ı": "ï",
    " ¨ı": "ï",
    " €O": "Ö",
    " €o": "ö",
    "¨o": "ö",
    "o ´": "ó",
    " €u": "ü",
    "€u": "ü",
    "/H20852": "]",
    "/H20851": "[",
    "/H20648": "",  # This is a double vertical line, probably can just remove it
    "/H18528": "⋅",
    "/H11350": "≥",
    "/H11349": "≤",
    "/H11022": ">",
    "/H11021": "<",
    " /H11006": "±",
    "/H11006": "±",
    "H11005": "=",
    "/H11002": "-",
    "/H11001": "+",
    "/H11011": "~",
    "/H9252": "β",
    "/H9251/": "a",  # Yes, just going to replace with "a" here instead of alpha
    " /H9004": "Δ",
    " /C226": "®",
    "/C226": "®",
    "/C224": "‡",
    "c /C223": "ç",
    "/C223": "©",
    "/C211": "©",
    "/C21": "≥",
    "/C20": "≤",
    " /C19E": "É",
    " /C6": "±",
    "/C6": "±",
    "/C3": "*",
    " /C1": ".",
    "/C1": ".",
    " /C0": "-",
    "/C0": "-",
    # Get rid of unknown unicodes last
    "": "",
}

PAGE_START_INDICATOR: str = "\nStart of Page {0}\n"
PAGE_END_INDICATOR: str = "\nEnd of Page {0}\n"


# ------------------------------
# LLM related constants
# ------------------------------
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
    "ARM.PCT.MALE",
    "ARM.AGE",
    "ARM.AGEU",
]

TIME_VALUE_HEADERS: List[str] = [
    "ARM.TIME1",
    "ARM.TIME1U",
]

STAT_GROUP_HEADERS: List[str] = [
    "STATANAL.POP",
    "STATANAL.METHOD",
    "STATANAL.IMP.METHOD",
]

CLINICAL_DATA_HEADERS: List[str] = [
    "N.ARM.STATANAL", # Number of subjects at each treatment arm at each time
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


# ------------------------------
# Prompting related constants
# ------------------------------
NO_DATA: str = "NO_DATA"

VAR_DICT: Dict[str, str] = {
    "Text_Start_Indicator": "[Clinical Trial Text Begins]\n",
    "Text_End_Indicator": "\n[Clinical Trial Text Ends]",
    "No_Data": NO_DATA,
}

OUTCOME_TYPE: Dict[int, str] = {
    0: "",  # Unknown
    1: "binary outcome (should only have values in RSP, not BSL, CHBSL, or PCHBSL) ",  # Binary outcome
    2: "",  # Continuous outcome
}


# ------------------------------
# CDF related constants
# ------------------------------

# Order of the headers in CSV
HEADER_ORDER = [
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

    "ARM.NUM",
    "ARM.BLIND",
    "ARM.RANDFLG",
    "ARM.TRT",
    "ARM.TRTCLASS",
    "ARM.DOSE",
    "ARM.DOSEU",
    "ARM.ROUTE",
    "ARM.REGIMEN",
    "ARM.FORMULATION",

    "N.STUDY",

    "N.ARM",

    "N.ARM.STATANAL",
    "N.ARM.EVENT.SUBJ",

    "STATANAL.POP",
    "STATANAL.METHOD",
    "STATANAL.IMP.METHOD",

    "ARM.TIME1",
    "ARM.TIME1U",

    "ENDPOINT",

    "BSL.STAT",
    "BSL.VAL",
    "BSL.VALU",
    "BSL.VAR",
    "BSL.VARU",
    "BSL.LCI",
    "BSL.UCI",
    "CHBSL.STAT",
    "CHBSL.VAL",
    "CHBSL.VALU",
    "CHBSL.VAR",
    "CHBSL.VARU",
    "CHBSL.LCI",
    "CHBSL.UCI",
    "RSP.STAT",
    "RSP.VAL",
    "RSP.VALU",
    "RSP.VAR",
    "RSP.VARU",
    "RSP.LCI",
    "RSP.UCI",
    "PCHBSL.STAT",
    "PCHBSL.VAL",
    "PCHBSL.VAR",
    "PCHBSL.VARU",
    "PCHBSL.LCI",
    "PCHBSL.UCI",
    
    "ARM.PCT.MALE",
    "ARM.AGE",
    "ARM.AGEU",
]

# Columns to ignore when comparing two CDFs.
CDF_COMPARE_COLS_IGNORE = ["DSID", "ARM.NUM"]

CDF_COMPOUND_KEY_COLS = ["ARM.TRT", "ARM.DOSE", "ARM.REG", "ENDPOINT"]

# ------------------------------
# Testing related constants
# ------------------------------
TEST_DATA_SUBFOLDER = "test_data"
TEST_DATA_SUFFIX = ".pdfdata"