from datetime import datetime
import logging
import os
import sys

from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from ..consts import (
    GREEN,
    NO_DATA,
    RESET,
    SILENCED_LOGGING_MODULES,
    VAR_DICT
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
        Don't call this by itself, this is used by some nested methods.
        '''
        prompt = self.config["Prompt Engineering"]["Prelude"] + "\n"
        prompt += self.config["Prompt Engineering"]["UserRole"] + ": "
        prompt += question + "\n"
        prompt += self.config["Prompt Engineering"]["HectreRole"] + ": "
        prompt += self.config["Prompt Engineering"]["Prefix"]
        return prompt
    
    
    def update_prompt(self, prompt: str, response: str, question: str):
        '''
        Update the prompt with the response and the new question.
        Use this for follow-up questions and multi-shot prompting.
        Don't call this by itself, this is used by some nested methods.
        '''
        prompt += response + "\n"
        prompt += self.config["Prompt Engineering"]["UserRole"] + ": "
        prompt += question + "\n"
        prompt += self.config["Prompt Engineering"]["HectreRole"] + ": "
        prompt += self.config["Prompt Engineering"]["Prefix"]
        return prompt
    

    def format_prompt(self, prompt: str, header_dict: Dict[str, str] = {}, extra_dict: Dict[str, str] = {}) -> str:
        '''
        Take a prompt from the YAML, and format it with variables.
        Don't call this by itself, this is used by some nested methods.
        '''
        format_dict = {}
        # First add some constants from VAR_DICT
        for key, val in VAR_DICT.items():
            if "{" + key + "}" in prompt:
                format_dict[key] = val
        # Now add headers in definitions
        for key, val in header_dict.items():
            key = key.replace(" ", "_")
            if "{" + key + "}" in prompt:
                format_dict[key] = val
        # Finally add whatever extra that was pased in
        for key, val in extra_dict.items():
            if "{" + key + "}" in prompt:
                format_dict[key] = val
        # Now do the string format
        try:
            prompt = prompt.format(**format_dict)
        except KeyError as e:
            logger.error(f"Could not format the prompt correctly: {prompt}")
            raise e
        return prompt
    
    
    def invoke_prompt_on_page(self, name: str, prompt_name: str, page: Page, page_num: int, header: Optional[str] = None, extra_vars: Optional[Dict[str, str]] = None) -> str:
        '''
        Wrapper to ask LLM about a specific thing (name) with a prompt in the YAML (prompt_name), on page (page) that corresponds to a header (header).
        
        Parameters:
            name (str): the name of the field, e.g. "authors", "treatment arms"
            prompt_name (str): the prompt to be used from the config.yaml file, e.g. "PromptLiterature", "PromptTreatmentArms"
            page
            page_num
            header (str): the related header in the CDF (if any)
        '''
        logger.info(f"Trying to fetch {name} from page {page_num + 1}...")
        header_dict = self.definitions.get_field_by_name(header) if header else {}
        extra_vars = extra_vars or {}
        prompt_num = 1
        prompt_key = f"{prompt_name}1"
        prior_content = ""
        response = ""
        # Iterate on each prompt
        while prompt_key in self.config["Prompt Engineering"]:
            prompt = self.config["Prompt Engineering"][prompt_key]
            extra_dict = {
                "Page_Num": f"{page_num + 1}",
                "Page_Text": page.get_text(),
            }
            extra_dict.update(extra_vars)
            prompt = self.format_prompt(prompt, header_dict=header_dict, extra_dict=extra_dict)
                
            # Now we have the prompt, now either create prompt from scratch or extend a previous conversation
            if not prior_content:
                prompt = self.build_new_prompt(prompt)
            else:
                prompt = self.update_prompt(prompt=prior_content, response=response, question=prompt)

            response = self.invoke_model(prompt)
            prior_content = prompt

            prompt_num += 1
            prompt_key = f"{prompt_name}{prompt_num}"

        if not response or NO_DATA in response:
            return ""
        logger.info(f"Got answer: {GREEN}{response}{RESET}")
        return response
    

    def query_literature_data(self, header: str, page: Page, page_num: int) -> Optional[str]:
        '''
        Construct the prompt(s) to get the literature data from the page using the LLM.
        '''
        header_dict = self.definitions.get_field_by_name(header)
        return self.invoke_prompt_on_page(name=header_dict['Field Label'], prompt_name="PromptLiterature", page=page, page_num=page_num, header=header)
    

    def query_treatment_arms(self, page: Page, page_num: int) -> List[str]:
        '''
        Get all the treatment arms, if they can be found on the page, as a list of strings.
        '''
        response = self.invoke_prompt_on_page(name="treatment arms", prompt_name="PromptTreatmentArms", page=page, page_num=page_num)
        ret = [arm.strip() for arm in response.split(';')]
        return list(set(ret))
    

    def query_time_values(self, page: Page, page_num: int) -> List[str]:
        '''
        Get all the nominal time values, if they can be found on the page, as a list of strings.
        '''
        response = self.invoke_prompt_on_page(name="time values", prompt_name="PromptTimeValues", page=page, page_num=page_num)
        ret = [arm.strip() for arm in response.split(';')]
        return list(set(ret))
    

    def query_clinical_data(self, header: str, outcome: str, treatment_arm: str, time_value: str, page: Page, page_num: int) -> Optional[str]:
        '''
        Construct the prompt(s) to get a specific clinical data from the page using the LLM.
        '''
        header_dict = self.definitions.get_field_by_name(header)
        extra_vars = {
            "Outcome": outcome,
            "Treatment_Arm": treatment_arm,
            "Time_Value": time_value,
        }
        return self.invoke_prompt_on_page(name=header_dict['Field Label'], prompt_name="PromptClinical", page=page, page_num=page_num, header=header, extra_vars=extra_vars)
