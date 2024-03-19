import logging

from pydantic import BaseModel
from typing import Any, Optional

from ..consts import NO_DATA
from ..ontology.definitions import Definitions
from ..pdf.page import Page
from ..models.consts import NAME_TO_MODEL_CLASS
from .config import Config

logger = logging.getLogger(__name__)

class HectreException(Exception):
    pass

class Hectre(BaseModel):
    '''
    The overarching class of the HECTRE project.
    HECTRE is able to either invoke the model, get literature data from a page,
    or clinical data from a page or table.
    '''
    config: Any = None
    definitions: Any = None
    llm: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = Config()
        try:
            llm_name = self.config["LLM"]["LLMName"]
        except KeyError:
            raise HectreException("Could not find LLMName in configuration!")
        self.set_llm(llm_name)
        self.llm.set_parameters_from_config(self.config)
        self.definitions = Definitions()

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
    
    def query_literature_data(self, header: str, page: Page, page_num: int) -> Optional[str]:
        '''
        Construct the prompt(s) to get the literature data from the page using the LLM.
        '''
        # TODO: Work on this
        readable_header = self.definitions.convert_to_readable_name(header)
        logger.info(f"Trying to fetch {readable_header} from page {page_num + 1}...")
        prompt = f'''Below is page {page_num + 1} from a clinical trial paper:

START OF PAGE
{page.get_text()}
END OF PAGE

I want to find the {readable_header.lower()}; here is a description of the thing I want: "{self.definitions.get_field_description(header)}". Please respond with just the answer with no other words, or with "{NO_DATA}".'''
        
        output = self.invoke_model(prompt)
        if NO_DATA in output:
            return None
        logger.info(f"Got answer: {output}")
        return output
