import os
import re

from hectre.consts import (
    TEST_DATA_SUBFOLDER,
    TEST_DATA_SUFFIX,
)
from hectre.input_parsers.pdfplumber_pypdf2_pdf_parser import PdfPlumberPypdf2PdfParser


def pdf_unicode_check(file_path):
    # Hardcode the parser here as we don't want to call the LLM for a test
    paper = PdfPlumberPypdf2PdfParser(file_path=file_path, url=None).parse()
    for page in paper.get_pages():
        assert not page.unknown_unicode_chars, f"Found unknown unicode character(s): {page.unknown_unicode_chars} (paper: {file_path}) (content: {page.get_text()})"
        for line in page.get_text().split("\n"):
            assert not re.search("/C[0-9]", line) and not re.search("/H[0-9]", line), f"Found unknown character(s) on line: {line} (paper: {file_path})"


def test_pdf_should_not_contain_unknown_unicode():
    '''
    Checks if the file processed by PDF extractor does not have
    any lingering unknown unicode characters.
    '''
    directory = os.path.join(os.path.dirname(__file__), "../../tests", TEST_DATA_SUBFOLDER)
    for filename in os.listdir(directory):
        if filename.endswith(TEST_DATA_SUFFIX):
            file_path = os.path.join(directory, filename)
            pdf_unicode_check(file_path)