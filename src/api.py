import logging

from .cdf.cdf import Cdf
from .consts import LITERATURE_DATA_HEADERS
from .input_parsers.page import Page
from .input_parsers.paper import Paper
from. input_parsers.pdf_parser import PdfParser
from .input_parsers.picos import Picos
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
    for col, canonical_header in enumerate(LITERATURE_DATA_HEADERS):
        # Convert these into human-readable (LLM-readable) header names
        header = hectre.get_readable_header(canonical_header)
        # Get the total number of pages, and try to extract that data from each page until we get something.
        num_pages = paper.get_num_pages()
        for page_num in range(1, num_pages + 1):
            page: Page = paper.get_page(page_num)

            result = hectre.query_literature_data(header=header, page=page, page_num=page_num)
            # If we got a non-null result, it means we found it.
            if result:
                # Set the value in the CDF
                cdf.set_value_for_paper_id(paper_id=paper_id, col=col, value=result)
                return


def extract_clinical_data(paper: Paper, picos: Picos, cdf: Cdf) -> None:
    '''
    Extract all the clinical data.
    Modifies the CDF in-place.
    '''
    # TODO
    pass


def extract_data(paper: Paper, picos: Picos) -> Cdf:
    '''
    Main entry function that is called by the front end to initiate the extraction
    process.
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


def extract_from_file_path(file_path: str, picos_string: str) -> Cdf:
    '''
    Overarching function to turn a file path and a PICOS string into a CDF object.
    '''
    pdf_parser = PdfParser.from_file(file_path)
    paper = pdf_parser.parse()
    picos = Picos(picos_string)
    return extract_data(paper, picos)


def extract_from_url(url: str, picos_string: str) -> Cdf:
    '''
    Overarching function to turn a URL and a PICOS string into a CDF object.
    '''
    pdf_parser = PdfParser.from_url(url)
    paper = pdf_parser.parse()
    picos = Picos(picos_string)
    return extract_data(paper, picos)