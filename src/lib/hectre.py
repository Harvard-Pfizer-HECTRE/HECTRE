from typing import Optional

from ..pdf.page import Page
from ..models.consts import NAME_TO_MODEL_CLASS
from .config import Config

class HectreException(Exception):
    pass

class Hectre:
    '''
    The overarching class of the HECTRE project.
    HECTRE is able to either invoke the model, get literature data from a page,
    or clinical data from a page or table.
    '''

    def __init__(self):
        self.config = Config()
        try:
            llm_name = self.config["LLM"]["LLMName"]
        except KeyError:
            raise HectreException("Could not find LLMName in configuration!")
        self.set_llm(llm_name)
        self.llm.set_parameters_from_config(self.config)

    def set_llm(self, llm_name: str) -> None:
        '''
        Set the LLM to be used by HECTRE.

        Parameters:
            llm_name (str)
        '''
        try:
            self.llm = NAME_TO_MODEL_CLASS[llm_name]()
        except KeyError:
            raise HectreException(f"{llm_name} is not a supported LLM type!")
        
    def invoke_model(self, prompt: str) -> str:
        '''
        Call the LLM to get an output.

        Parameters:
            prompt (str)

        Returns:
            str
        '''
        return self.llm.invoke(prompt)
    
    def get_readable_header(self, canonical_header: str) -> str:
        '''
        The headers in the CDF files may not be understood by LLM, so convert
        them to a readable header.

        Ex: AU converts to Authors, PY converts to Publishing Year.

        Parameters:
            canonical_header (str)

        Returns:
            str
        '''
        # TODO
        return canonical_header
    
    def query_literature_data(self, header: str, page: Page, page_num: int) -> Optional[str]:
        '''
        Construct the prompt(s) to get the literature data from the page using the LLM.
        '''
        # TODO