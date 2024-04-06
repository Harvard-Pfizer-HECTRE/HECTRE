import logging

import json
import json5

from .cdf.cdf import CDF, CDFData
from .consts import (
    CLINICAL_DATA_HEADERS,
    NO_DATA,
    PER_TREATMENT_ARM_HEADERS,
    PER_TREATMENT_ARM_PER_TIME_HEADERS,
)
from .pdf.page import Page
from .pdf.paper import Paper
from. input_parsers.pdf_parser import PdfParser
from. input_parsers.picos_parser import PicosParser
from .picos.picos import Picos
from .lib.hectre import Hectre

logger = logging.getLogger(__name__)

# Global HECTRE singleton
hectre = Hectre()

def invoke_model(prompt):
    '''
    Invoke the model, following the configuration file.
    This is mostly just used for testing.

    Parameters:
        prompt (str): The prompt for the model.

    Returns:
        str: The output from the model.
    '''
    return hectre.invoke_model(prompt)


def extract_literature_data_whole_paper(paper: Paper, picos: Picos, cdf: CDF) -> None:
    '''
    Extract all the literature data such as authors, title, etc.
    Modifies the CDF in-place.
    '''
    text = paper.get_all_text()
    text_context = "text"
    result = hectre.query_literature_data(text=text, text_context=text_context)
    if result:
        try:
            literature_data_json = json5.loads(result)
        except json.JSONDecodeError as e:
            logger.error(f"Could not decode literature data output: {result}")
            raise e
        
    literature_data_json["DSID"] = paper.get_id()
                
    cd = CDFData.from_dicts(literature_data_json)
    cdf.set_literature_data(cd)
    

def extract_clinical_data_whole_paper(paper: Paper, picos: Picos, cdf: CDF) -> None:
    '''
    Extract all the clinical data.
    Modifies the CDF in-place.
    '''

    paper_id = paper.get_id()
    outcomes = picos.outcomes
    text = paper.get_all_text()
    text_context = f"text"

    # Get all the treatment arms in the paper
    treatment_arms = hectre.query_treatment_arms(text=text, text_context=text_context)

    if not treatment_arms:
        logger.error(f"Could not find any treatment arms for paper {paper_id}!")
        # Technically we won't have any rows if there are no treatment arms, but we
        # don't want to throw either because we may be processing multiple papers.
        # This means extracting from this paper has essentially failed.
        return

    # Get all the nominal time values
    time_values = hectre.query_time_values(text=text, text_context=text_context)

    if not time_values:
        logger.error(f"Could not find any time values for paper {paper_id}!")
        return
    
    # Get all the statistical analysis groups
    stat_groups_res = hectre.query_stat_groups(text=text, text_context=text_context)

    try:
        stat_groups = json5.loads(stat_groups_res)
    except json.JSONDecodeError as e:
        logger.error(f"Could not decode statistical analysis groups data output: {result}")
        # This stat groups is broken
        return

    placebo_arm_found: bool = False
    current_arm_counter: int = 1
    # Loop through every treatment arm
    for treatment_arm in treatment_arms:
        # Set the ARM.NUM here. We only expect one Placebo arm, which will be designated 0
        # All other arms go in incremental order, and doesn't really matter the order
        current_arm_num = current_arm_counter
        if not placebo_arm_found and "placebo" in treatment_arm.lower():
            current_arm_num = 0
            placebo_arm_found = True
        else:
            current_arm_counter += 1
        arm_data_dict = {"ARM.NUM": current_arm_num}

        # First let's populate some information pertaining to each treatment arm
        result = hectre.query_per_treatment_arm_data(text=text, headers=PER_TREATMENT_ARM_HEADERS, treatment_arm=treatment_arm, text_context=text_context)
        # If we got any results, load it as JSON object, and update our JSON for this clinical data row
        try:
            per_treatment_arm_data_json = json5.loads(result)
        except json.JSONDecodeError as e:
            logger.error(f"Could not decode per-treatment arm data output: {result}")
            # This treatment arm is broken, but let's continue to the next one
            continue

        # filter out any not-expected entries in the JSON
        for key, val in per_treatment_arm_data_json.items():
            if key not in PER_TREATMENT_ARM_HEADERS:
                logger.error(f"Invalid per-treatment arm entry {key}: {val}")
        # Add the entries
        arm_data_dict.update({key: val for key, val in per_treatment_arm_data_json.items() if key in PER_TREATMENT_ARM_HEADERS})

        # Loop through every time value
        for time_value in time_values:
            time_data_dict = {'ARM.TIME1': time_value, "ARM_TIME1U": ""}
            # Loop through every outcome
            for outcome in outcomes:
                outcome_dict = {"ENDPOINT": outcome}
                # Loop through every stat group
                for stat_group in stat_groups:
                    result = hectre.query_clinical_data(headers=CLINICAL_DATA_HEADERS, outcome=outcome, treatment_arm=treatment_arm, time_value=time_value, stat_group=stat_group, text=text, text_context=text_context)
                    # If we got any results, load it as JSON object, and update our JSON for this clinical data row
                    try:
                        clinical_data_json = json5.loads(result)
                    except json.JSONDecodeError as e:
                        logger.error(f"Could not decode clinical data output: {result}")
                        # We keep going
                        continue
                    
                    # Finally, set the value in the CDF for this one row
                    cd = CDFData.from_dicts(arm_data_dict, time_data_dict, outcome_dict, stat_group, clinical_data_json)
                    cdf.add_clinical_data(cd)
    

def extract_data_from_objects(paper: Paper, picos: Picos) -> CDF:
    '''
    Main entry function that initiates the extraction process.
    TODO: Finish this function up

    Parameters:
        paper (Paper)
        picos (Picos)

    Returns:
        No output. This function will take a while, so we will store the output elsewhere.
    '''
    cdf = CDF()
    extract_literature_data_whole_paper(paper, picos, cdf)
    extract_clinical_data_whole_paper(paper, picos, cdf)
    return cdf


def extract_data(file_path: str = None, url: str = None, picos_string: str = None) -> CDF:
    '''
    Overarching function to turn a file path and a PICOS string into a CDF object.
    '''
    pdf_parser = PdfParser(file_path=file_path, url=url)
    paper = pdf_parser.parse()
    picos_parser = PicosParser(picos_string=picos_string)
    picos = picos_parser.parse()
    return extract_data_from_objects(paper, picos)
