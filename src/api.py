import logging

import json
import json5

from .cdf.cdf import CDF, ClinicalData
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


def extract_literature_data(paper: Paper, picos: Picos, cdf: CDF) -> None:
    '''
    Extract all the literature data such as authors, title, etc.
    Modifies the CDF in-place.
    '''
    if hectre.whole_paper:
        text  = paper.get_all_text()
        text_context = "text"
        result = hectre.query_literature_data(text=text, text_context=text_context)
        if result:
            try:
                literature_data_json = json5.loads(result)
            except json.JSONDecodeError as e:
                logger.error(f"Could not decode literature data output: {result}")
                raise e
    else:
        # Get the total number of pages, and try to extract that data from each page until we get something.
        literature_data_json = {}
        num_pages = paper.get_num_pages()
        for page_num in range(num_pages):
            page: Page = paper.get_page(page_num)
            text = page.get_text()
            text_context = f"page {page_num + 1}"
            
            result = hectre.query_literature_data(text=text, text_context=text_context)
            # If we got a non-null result, it means we found it.
            if result:
                try:
                    result_json = json5.loads(result)
                    literature_data_json = hectre.combine_dicts(literature_data_json, result_json)
                    if not NO_DATA in literature_data_json.values():
                        # If all fields are filled, we can exit early
                        break
                except json.JSONDecodeError as e:
                    logger.error(f"Could not decode literature data output: {result}")
                    raise e
                
    cdf.set_literature_data(literature_data_json)
    


def extract_clinical_data(paper: Paper, picos: Picos, cdf: CDF) -> None:
    '''
    Extract all the clinical data.
    Modifies the CDF in-place.
    '''

    paper_id = paper.get_id()
    num_pages = paper.get_num_pages()

    outcomes = picos.outcomes

    # Get all the treatment arms in the paper
    treatment_arms = []
    for page_num in range(num_pages):
        page: Page = paper.get_page(page_num)
        text = page.get_text()
        text_context = f"page {page_num + 1}"

        treatment_arms = hectre.query_treatment_arms(text=text, text_context=text_context)
        # If we got a non-empty result, it means we found it.
        if treatment_arms:
            break
    if not treatment_arms:
        logger.error(f"Could not find any treatment arms for paper {paper_id}!")
        # Technically we won't have any rows if there are no treatment arms, but we
        # don't want to throw either because we may be processing multiple papers.
        # This means extracting from this paper has essentially failed.
        return

    # Get all the nominal time values
    time_values = []
    for page_num in range(num_pages):
        page: Page = paper.get_page(page_num)
        text = page.get_text()
        text_context = f"page {page_num + 1}"

        time_values = hectre.query_time_values(text=text, text_context=text_context)
        # If we got a non-empty result, it means we found it.
        if time_values:
            break
    if not time_values:
        logger.error(f"Could not find any time values for paper {paper_id}!")

    # Loop through every treatment arm
    for treatment_arm in treatment_arms:
        # First let's populate some information pertaining to each treatment arm
        per_treatment_arm_data_json = {}
        num_pages = paper.get_num_pages()
        for page_num in range(num_pages):
            page: Page = paper.get_page(page_num)
            text_context = f"page {page_num + 1}"
            text = page.get_text()
            result = hectre.query_per_treatment_arm_data(text=text, headers=PER_TREATMENT_ARM_HEADERS, treatment_arm=treatment_arm, text_context=text_context)
            # If we got any results, load it as JSON object, and update our JSON for this clinical data row
            if result:
                try:
                    result_json = json5.loads(result)
                    per_treatment_arm_data_json = hectre.combine_dicts(per_treatment_arm_data_json, result_json)
                    if not NO_DATA in per_treatment_arm_data_json.values():
                        # If all fields are filled, we can exit early
                        break
                except json.JSONDecodeError as e:
                    logger.error(f"Could not decode per-treatment arm data output: {result}")
                    raise e

        # TODO: Add the per-arm result to CDF

        # Loop through every time value
        for time_value in time_values:
            # Let's populate some information per-treatment-arm and per-time
            per_treatment_arm_per_time_json = {}
            num_pages = paper.get_num_pages()
            for page_num in range(num_pages):
                page: Page = paper.get_page(page_num)
                text_context = f"page {page_num + 1}"
                text = page.get_text()
                result = hectre.query_per_treatment_arm_per_time_data(text=text, headers=PER_TREATMENT_ARM_PER_TIME_HEADERS, treatment_arm=treatment_arm, time_value=time_value, text_context=text_context)
                # If we got any results, load it as JSON object, and update our JSON for this clinical data row
                if result:
                    try:
                        result_json = json5.loads(result)
                        per_treatment_arm_per_time_json = hectre.combine_dicts(per_treatment_arm_per_time_json, result_json)
                        if not NO_DATA in per_treatment_arm_per_time_json.values():
                            # If all fields are filled, we can exit early
                            break
                    except json.JSONDecodeError as e:
                        logger.error(f"Could not decode per-treatment arm per-time data output: {result}")
                        raise e
                    
            # TODO: Add the per-arm per-time result to CDF

            # Loop through every outcome
            arm_data = {'ARM.TIME1': time_value, 'ARM.TRT': treatment_arm}
            for outcome in outcomes:
                clinical_data_json = {}
                # Loop through every page
                for page_num in range(num_pages):
                    page: Page = paper.get_page(page_num)
                    # Only if the page has tables
                    if page.get_has_table():
                        text_context = f"page {page_num + 1}"
                        text = page.get_text()
                        result = hectre.query_clinical_data(headers=CLINICAL_DATA_HEADERS, outcome=outcome, treatment_arm=treatment_arm, time_value=time_value, text=text, text_context=text_context)
                        # If we got any results, load it as JSON object, and update our JSON for this clinical data row
                        if result:
                            try:
                                result_json = json5.loads(result)
                                clinical_data_json = hectre.combine_dicts(clinical_data_json, result_json)
                                if not NO_DATA in clinical_data_json.values():
                                    # If all fields are filled, we can exit early
                                    break
                            except json.JSONDecodeError as e:
                                logger.error(f"Could not decode clinical data output: {result}")
                                raise e
                
                # Finally, set the value in the CDF for this one row
                cd = ClinicalData.from_json(json.dumps(clinical_data_json), json.dumps(arm_data))
                cdf.clinical_data.append(cd)


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
    extract_literature_data(paper, picos, cdf)
    extract_clinical_data(paper, picos, cdf)
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
