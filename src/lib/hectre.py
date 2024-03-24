from datetime import datetime
import logging
import os
import sys

from pydantic import BaseModel
from typing import Any, List, Optional

from ..consts import (
    GREEN,
    NO_DATA,
    RESET,
    SILENCED_LOGGING_MODULES
)
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
        self.set_up_logging()
        try:
            llm_name = self.config["LLM"]["LLMName"]
        except KeyError:
            raise HectreException("Could not find LLMName in configuration!")
        self.set_llm(llm_name)
        self.llm.set_parameters_from_config(self.config)
        self.definitions = Definitions()


    def set_up_logging(self) -> None:
        '''
        Set up everything related to logging.
        '''
        rootLogger = logging.getLogger()

        # Silence some specific modules
        for log_name, log_obj in logging.Logger.manager.loggerDict.items():
            if any([disabled_log_name in log_name for disabled_log_name in SILENCED_LOGGING_MODULES]):
                log_obj.disabled = True

        # Set up the file logger that prints to a log file
        # Will create a different file for every time HECTRE is initialized
        log_folder_path = os.path.join(os.path.dirname(__file__), "../../logs")
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        log_file_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".log"
        fileHandler = logging.FileHandler(log_folder_path + "/" + log_file_name, encoding='utf8')
        fileHandler.setLevel(self.config["General"]["FileLoggingLevel"])
        fileHandler.setFormatter(logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-4.8s] %(message)s"))
        rootLogger.addHandler(fileHandler)

        # Set up the stdout logger that prints to screen
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(self.config["General"]["ConsoleLoggingLevel"])
        consoleHandler.setFormatter(logging.Formatter("%(message)s"))
        rootLogger.addHandler(consoleHandler)

        rootLogger.setLevel("DEBUG")


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
    
    
    def build_new_prompt(self, question: str) -> str:
        '''
        Wrap the actual question to ask in some pre-made prompt engineering.
        '''
        prompt = self.config["Prompt Engineering"]["Prelude"] + "\n"
        prompt += self.config["Prompt Engineering"]["UserRole"] + ": "
        prompt += self.config["Prompt Engineering"]["Prefix"] + question + "\n"
        prompt += self.config["Prompt Engineering"]["HectreRole"] + ": "
        return prompt
    
    
    def update_prompt(self, prompt: str, response: str, question: str):
        '''
        Update the prompt with the response and the new question.
        Use this for follow-up questions and multi-shot prompting.
        '''
        prompt += response + "\n"
        prompt += self.config["Prompt Engineering"]["UserRole"] + ": "
        prompt += self.config["Prompt Engineering"]["Prefix"] + question + "\n"
        prompt += self.config["Prompt Engineering"]["HectreRole"] + ": "
        return prompt
    

    def query_literature_data(self, header: str, page: Page, page_num: int) -> Optional[str]:
        '''
        Construct the prompt(s) to get the literature data from the page using the LLM.
        '''
        readable_header = self.definitions.convert_to_readable_name(header)
        logger.info(f"Trying to fetch {readable_header} from page {page_num + 1}...")

        question = f'''Below is page {page_num + 1} from a clinical trial paper:

START OF PAGE
{page.get_text()}
END OF PAGE

I want to find the {readable_header.lower()}; here is a description of the thing I want: "{self.definitions.get_field_description(header)}". Please respond with just the answer with no other words, or with "{NO_DATA}".
'''

        prompt = self.build_new_prompt(question)
        
        output = self.invoke_model(prompt)
        if NO_DATA in output:
            return None
        logger.info(f"Got answer: {GREEN}{output}{RESET}")
        return output
    

    def query_treatment_arms(self, page: Page, page_num: int) -> List[str]:
        '''
        Get all the treatment arms, if they can be found on the page, as a list of strings.
        '''

        logger.info(f"Trying to fetch treatment arms from page {page_num + 1}...")
        question = f'''Below is page {page_num + 1} from a clinical trial paper:

START OF PAGE
{page.get_text()}
END OF PAGE

I want to find all the treatment arms in the paper. Please respond with just the answer, with each treatment arm separated by semi-colon with no other words, or with "{NO_DATA}" if they cannot be deduced from this page.
'''
        prompt = self.build_new_prompt(question)
        
        output = self.invoke_model(prompt)
        if NO_DATA in output:
            return []
        logger.info(f"Got answer: {GREEN}{output}{RESET}")
        ret = [arm.strip() for arm in output.split(';')]
        return list(set(ret))
    

    def query_time_values(self, page: Page, page_num: int) -> List[str]:
        '''
        Get all the nominal time values, if they can be found on the page, as a list of strings.
        '''

        logger.info(f"Trying to fetch nominal time values from page {page_num + 1}...")
        question = f'''Below is page {page_num + 1} from a clinical trial paper:

START OF PAGE
{page.get_text()}
END OF PAGE

I want to find all the nominal time values for treatments in the paper. Please respond with just the time values, with each separated by semi-colon with no other words, or with "{NO_DATA}" if they cannot be deduced from this page.
'''
        prompt = self.build_new_prompt(question)
        
        output = self.invoke_model(prompt)
        if NO_DATA in output:
            return []
        logger.info(f"Got answer: {GREEN}{output}{RESET}")
        ret = [val.strip() for val in output.split(';')]
        return list(set(ret))
    

    def query_clinical_data(self, header: str, outcome: str, treatment_arm: str, time_value: str, page: Page, page_num: int) -> Optional[str]:
        '''
        Construct the prompt(s) to get a specific clinical data from the page using the LLM.
        '''
        readable_header = self.definitions.convert_to_readable_name(header)
        logger.info(f"Trying to fetch {readable_header} at time {time_value} for arm {treatment_arm} for outcome {outcome} from page {page_num + 1}...")

        question = f'''Below is page {page_num + 1} from a clinical trial paper:

START OF PAGE
{page.get_text()}
END OF PAGE

I want to find the exact {readable_header.lower()} for {treatment_arm} at time {time_value} for endpoint {outcome}; here is a description of the thing I want: "{self.definitions.get_field_description(header)}". Please respond with just the answer with no other words, or with "{NO_DATA}".
'''

        prompt = self.build_new_prompt(question)
        
        output = self.invoke_model(prompt)
        if NO_DATA in output:
            return None
        logger.info(f"Got answer: {GREEN}{output}{RESET}")
        return output
