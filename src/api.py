import logging

from .cdf.cdf import Cdf
from .consts import (
    LITERATURE_DATA_HEADERS,
    SKIPPED_LITERATURE_DATA_HEADERS,
)
from .pdf.page import Page
from .pdf.paper import Paper
from. input_parsers.pdf_parser import PdfParser
from .picos.picos import (
    Picos,
    Population,
)
from .lib.hectre import Hectre

logger = logging.getLogger(__name__)

# Global HECTRE singleton
hectre = None

def invoke_model(prompt):
    '''
    Invoke the model, following the configuration file.
    This is mostly just used for testing.

    Parameters:
        prompt (str): The prompt for the model.

    Returns:
        str: The output from the model.
    '''
    global hectre
    if hectre is None:
        hectre = Hectre()

    return hectre.invoke_model(prompt)


def extract_literature_data(paper: Paper, picos: Picos, cdf: Cdf) -> None:
    '''
    Extract all the literature data such as authors, title, etc.
    Modifies the CDF in-place.
    '''

    paper_id = paper.get_id()

    # First, loop over every literature data header we need in CDF
    for col, header in enumerate(LITERATURE_DATA_HEADERS):
        if header in SKIPPED_LITERATURE_DATA_HEADERS:
            continue

        # Some headers we skip, for one reason or another
        if header is None:
            continue

        # Get the total number of pages, and try to extract that data from each page until we get something.
        num_pages = paper.get_num_pages()
        for page_num in range(num_pages):
            page: Page = paper.get_page(page_num)

            result = hectre.query_literature_data(header=header, page=page, page_num=page_num)
            # If we got a non-null result, it means we found it.
            if result:
                # Set the value in the CDF
                # TODO
                break


def extract_clinical_data(paper: Paper, picos: Picos, cdf: Cdf) -> None:
    '''
    Extract all the clinical data.
    Modifies the CDF in-place.
    '''
    # TODO

    paper_id = paper.get_id()
    num_pages = paper.get_num_pages()

    outcomes = ["HbA1c"] # Hardcode this for testing

    # Get all the treatment arms in the paper
    treatment_arms = []
    for page_num in range(num_pages):
        page: Page = paper.get_page(page_num)
        treatment_arms = hectre.query_treatment_arms(page=page, page_num=page_num)
        # If we got a non-empty result, it means we found it.
        if treatment_arms:
            break
    if not treatment_arms:
        logger.error(f"Could not find any treatment arms for paper {paper_id}!")

    # Get all the nominal time values
    time_values = []
    for page_num in range(num_pages):
        page: Page = paper.get_page(page_num)
        time_values = hectre.query_time_values(page=page, page_num=page_num)
        # If we got a non-empty result, it means we found it.
        if time_values:
            break
    if not time_values:
        logger.error(f"Could not find any time values for paper {paper_id}!")

    # Loop through every outcome
    for outcome in outcomes:
        # Loop through every treatment arm
        for treatment_arm in treatment_arms:
            # Loop through every time value
            for time_value in time_values:

                # Hardcode one specific clinical data value we want to find, as a test
                # Start on page 2, as a test, to make results better
                for page_num in range(1, num_pages):
                    page: Page = paper.get_page(page_num)

                    result = hectre.query_clinical_data(header="RSP.VAL", outcome=outcome, treatment_arm=treatment_arm, time_value=time_value, page=page, page_num=page_num)
                    # If we got a non-null result, it means we found it.
                    if result:
                        # Set the value in the CDF
                        # TODO
                        break


def extract_data_from_objects(paper: Paper, picos: Picos) -> Cdf:
    '''
    Main entry function that initiates the extraction process.
    TODO: Finish this function up

    Parameters:
        paper (Paper)
        picos (Picos)

    Returns:
        No output. This function will take a while, so we will store the output elsewhere.
    '''
    global hectre
    if hectre is None:
        hectre = Hectre()

    cdf = Cdf()

    extract_literature_data(paper, picos, cdf)

    extract_clinical_data(paper, picos, cdf)

    return cdf


def extract_data(file_path: str = None, url: str = None, picos_string: str = None) -> Cdf:
    '''
    Overarching function to turn a file path and a PICOS string into a CDF object.
    '''
    pdf_parser = PdfParser(file_path=file_path, url=url)
    paper = pdf_parser.parse()
    # TODO for PICOS
    picos = Picos(population=Population(disease="", sub_populations=set()), interventions=set(), comparators=set(), outcomes=set(), study_designs=set())
    return extract_data_from_objects(paper, picos)