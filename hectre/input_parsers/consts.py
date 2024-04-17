from typing import Any, Dict

from hectre.input_parsers.llm_pypdf2_pdf_parser import LlmPypdf2PdfParser
from hectre.input_parsers.pdfplumber_llm_pypdf2_pdf_parser import PdfPlumberLlmPypdf2PdfParser
from hectre.input_parsers.pdfplumber_pypdf2_pdf_parser import PdfPlumberPypdf2PdfParser
from hectre.input_parsers.pdfplumber_pypdfium2_pdf_parser import PdfPlumberPypdfium2PdfParser
from hectre.input_parsers.pymupdf_pdf_parser import PymupdfPdfParser


NAME_TO_PDF_PARSER: Dict[str, Any] = {
    "LlmPypdf2PdfParser": LlmPypdf2PdfParser,
    "PdfPlumberLlmPypdf2PdfParser": PdfPlumberLlmPypdf2PdfParser,
    "PdfPlumberPypdf2PdfParser": PdfPlumberPypdf2PdfParser,
    "PymupdfPdfParser": PymupdfPdfParser,
    "PdfPlumberPypdfium2PdfParser": PdfPlumberPypdfium2PdfParser,
}