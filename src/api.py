import logging

from .cdf.cdf import Cdf
from .consts import (
    LITERATURE_DATA_HEADERS,
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


def extract_literature_data(paper: Paper, picos: Picos, cdf: Cdf) -> None:
    '''
    Extract all the literature data such as authors, title, etc.
    Modifies the CDF in-place.
    '''

    paper_id = paper.get_id()

    # First, loop over every literature data header we need in CDF
    for header in LITERATURE_DATA_HEADERS:
        # Get the total number of pages, and try to extract that data from each page until we get something.
        num_pages = paper.get_num_pages()
        for page_num in range(num_pages):
            page: Page = paper.get_page(page_num)
            text = page.get_text()
            text_context = f"page {page_num + 1}"

            result = hectre.query_literature_data(header=header, text=text, text_context=text_context)
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
        for header in PER_TREATMENT_ARM_HEADERS:
            # Get the total number of pages, and try to extract that data from each page until we get something.
            num_pages = paper.get_num_pages()
            for page_num in range(num_pages):
                page: Page = paper.get_page(page_num)

                # TODO: Add function in hectre to query per-treatment arm data
                # TODO: Then add the result to CDF

        # Loop through every time value
        for time_value in time_values:
            # Let's populate some information per-treatment-arm and per-time
            for header in PER_TREATMENT_ARM_PER_TIME_HEADERS:
                # Get the total number of pages, and try to extract that data from each page until we get something.
                num_pages = paper.get_num_pages()
                for page_num in range(num_pages):
                    page: Page = paper.get_page(page_num)

                    # TODO: Add function in hectre to query per-treatment arm and per-time data
                    # TODO: Then add the result to CDF

            # Loop through every outcome
            for outcome in outcomes:

                # TODO: Work on this, and iterate through all clinical data headers
                # Hardcode one specific clinical data value we want to find, as a test
                # Start on page 2, as a test, to make results better
                # Ideally we want to query all of the clinical data columns here.
                for page_num in range(1, num_pages):
                    page: Page = paper.get_page(page_num)
                    text = page.get_text()
                    text_context = f"page {page_num + 1}"

                    result = hectre.query_clinical_data(header="RSP.VAL", outcome=outcome, treatment_arm=treatment_arm, time_value=time_value, text=text, text_context=text_context)
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
    picos_parser = PicosParser(picos_string=picos_string)
    picos = picos_parser.parse()
    return extract_data_from_objects(paper, picos)