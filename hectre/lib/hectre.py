from datetime import datetime
import logging
import os
import sys

from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from hectre.consts import (
    GREEN,
    LITERATURE_DATA_HEADERS,
    NO_DATA,
    OUTCOME_TYPE,
    RESET,
    SILENCED_LOGGING_MODULES,
    STAT_GROUP_HEADERS,
    TIME_VALUE_HEADERS,
    VAR_DICT
)
from hectre.lib.config import Config
from hectre.models.consts import NAME_TO_MODEL_CLASS
from hectre.ontology.definitions import Definitions

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


    def invoke_model(self, prompt: List[str]) -> str:
        '''
        Call the LLM to get an output.

        Parameters:
            prompt (List[str])

        Returns:
            str
        '''
        return self.llm.invoke(prompt)
    

    def combine_dicts(self, dict1: Dict[str, str], dict2: Dict[str, str]) -> Dict[str, str]:
        '''
        Combine two resultant dictionaries returned by the model. Since we care about "NO_DATA",
        we need this custom combine function.
        '''
        outdict = {}
        outdict.update(dict1)
        for key, val in dict2.items():
            if not key in outdict:
                outdict[key] = val
            else:
                # Only update if dict 1 has NO_DATA and dict 2 has data
                if not NO_DATA in val and NO_DATA in outdict[key]:
                    outdict[key] = val
        return outdict


    def build_new_prompt(self, question: str) -> str:
        '''
        Wrap the actual question to ask in some pre-made prompt engineering.
        Don't call this by itself, this is used by some nested methods.
        '''
        prompt = self.config["Prompt Engineering"]["Prelude"] + "\n"
        if self.llm.USER_ASSISTANT_MODEL:
            prompt += question + "\n" + self.config["Prompt Engineering"]["Prefix"]
        else:
            prompt += self.config["Prompt Engineering"]["UserRole"] + ": "
            prompt += question + "\n"
            prompt += self.config["Prompt Engineering"]["Prefix"] + "\n"
            prompt += self.config["Prompt Engineering"]["HectreRole"] + ": "
        return prompt


    def update_prompt(self, prior_content: List[str], response: str, question: str) -> List[str]:
        '''
        Update the prompt with the response and the new question.
        Use this for follow-up questions and multi-shot prompting.
        Don't call this by itself, this is used by some nested methods.
        '''
        if self.llm.USER_ASSISTANT_MODEL:
            prompt = prior_content.copy()
            prompt.append(response)
            prompt.append(question)
        else:
            prompt = prior_content[0][:-(len(self.config["Prompt Engineering"]["Prefix"]) + len(self.config["Prompt Engineering"]["HectreRole"]) + 4)]
            prompt += "\n" + self.config["Prompt Engineering"]["HectreRole"] + ": "
            prompt += response + "\n"
            prompt += self.config["Prompt Engineering"]["UserRole"] + ": "
            prompt += question + "\n"
            prompt += self.config["Prompt Engineering"]["Prefix"] + "\n"
            prompt += self.config["Prompt Engineering"]["HectreRole"] + ": "
            prompt = [prompt]
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


    def invoke_prompt_on_text(self, name: str, prompt_name: str, text: str, text_context: str, header: Optional[str] = None, extra_vars: Optional[Dict[str, str]] = None, keep_no_data_response: bool = False) -> str:
        '''
        Wrapper to ask LLM about a specific thing (name) with a prompt in the YAML (prompt_name), on text that corresponds to a header (header).

        Parameters:
            name (str): the name of the field, e.g. "authors", "treatment arms"
            prompt_name (str): the prompt to be used from the config.yaml file, e.g. "PromptLiterature", "PromptTreatmentArms"
            text (str): the text to query from, could be table, page, multiple pages adjoined, etc.
            text_context (str): the context of the text, e.g. "page 5", "table 2"
            header (str): the related header in the CDF (if any)
        '''
        logger.info(f"Trying to fetch {name} from {text_context}...")
        header_dict = self.definitions.get_field_by_name(header) if header else {}
        extra_vars = extra_vars or {}
        prompt_num = 1
        prompt_key = f"{prompt_name}1"
        prior_content = []
        response = ""
        # Iterate on each prompt
        while prompt_key in self.config["Prompt Engineering"]:
            prompt = self.config["Prompt Engineering"][prompt_key]
            extra_dict = {
                "Text_Context": text_context,
                "Text": text,
            }
            extra_dict.update(extra_vars)
            prompt = self.format_prompt(prompt, header_dict=header_dict, extra_dict=extra_dict)

            # Now we have the prompt, now either create prompt from scratch or extend a previous conversation
            if not prior_content:
                prompt_in = [self.build_new_prompt(prompt)]
            else:
                prompt_in = self.update_prompt(prior_content=prior_content, response=response, question=prompt)
            response = self.invoke_model(prompt_in)
            prior_content = prompt_in

            prompt_num += 1
            prompt_key = f"{prompt_name}{prompt_num}"

        if not keep_no_data_response and (not response or NO_DATA in response):
            return ""
        logger.info(f"Got answer: {GREEN}{response}{RESET}")
        return response
    

    def get_json_template_string_for_data_extraction(self, headers: List[str]) -> str:
        '''
        Construct the JSON template to feed into the LLM, with all the headers it should output.
        '''
        clinical_json = "{\n"
        for header in headers:
            header_dict = self.definitions.get_field_by_name(header)
            header_name = header_dict['Field Name']
            header_label = header_dict['Field Label']
            header_description = header_dict['Field Description']
            clinical_json += f'  "{header_name}": "",  # {header_label}. {header_description}\n'
        clinical_json += "}"
        return clinical_json


    def query_literature_data(self, text: str, text_context: str) -> Optional[str]:
        '''
        Construct the prompt(s) to get the literature data from the page using the LLM.
        '''
        name = "literature data"
        clinical_json = self.get_json_template_string_for_data_extraction(LITERATURE_DATA_HEADERS)
        extra_vars = {
            "Template": clinical_json,
        }
        return self.invoke_prompt_on_text(name=name, prompt_name="PromptLiterature", text=text, text_context=text_context, extra_vars=extra_vars, keep_no_data_response=True)


    def query_treatment_arms(self, text: str, text_context: str) -> List[str]:
        '''
        Get all the treatment arms, if they can be found on the page, as a list of strings.
        '''
        response = self.invoke_prompt_on_text(name="treatment arms", prompt_name="PromptTreatmentArms", text=text, text_context=text_context)
        if not response:
            return []
        ret = [arm.strip() for arm in response.split(';')]
        return list(set(ret))


    def query_per_treatment_arm_data(self, text: str, headers: List[str], treatment_arm: str, text_context: str) -> str:
        '''
        Get all the per-treatment arm data.
        '''
        name = f"per-arm data for {treatment_arm}"
        clinical_json = self.get_json_template_string_for_data_extraction(headers)
        extra_vars = {
            "Treatment_Arm": treatment_arm,
            "Template": clinical_json,
        }
        return self.invoke_prompt_on_text(name=name, prompt_name="PromptPerTreatmentArm", text=text, text_context=text_context, extra_vars=extra_vars, keep_no_data_response=True)


    def query_time_values(self, text: str, text_context: str) -> List[str]:
        '''
        Get all the nominal time values, if they can be found on the page, as a list of strings.
        '''
        response = self.invoke_prompt_on_text(name="time values", prompt_name="PromptTimeValues", text=text, text_context=text_context)
        if not response:
            return []
        ret = list(filter(None, [arm.strip() for arm in response.split(';')]))
        return list(set(ret))
    

    def query_stat_groups(self, outcome: str, text: str, text_context: str) -> str:
        '''
        Get all the statistical analysis groups, as a list of dictionaries.
        '''
        clinical_json = self.get_json_template_string_for_data_extraction(STAT_GROUP_HEADERS)
        extra_vars = {
            "Outcome": outcome,
            "Template": clinical_json,
        }
        return self.invoke_prompt_on_text(name=f"statistical analysis groups for {outcome}", prompt_name="PromptStatGroups", text=text, text_context=text_context, extra_vars=extra_vars, keep_no_data_response=True)
    

    def query_outcome_type(self, outcome: str) -> str:
        '''
        Ask about the type that the outcome is, so we can better determine what types of data we should be getting.
        '''
        extra_vars = {
            "Outcome": outcome,
        }
        ret = self.invoke_prompt_on_text(name=f"{outcome} type", prompt_name="PromptOutcomeType", text="", text_context="LLM", extra_vars=extra_vars)
        try:
            outcome_type_int = int(ret)
        except ValueError:
            logger.error(f"Could not determine outcome type from response: {ret}")
            outcome_type_int = 0
        if outcome_type_int not in OUTCOME_TYPE:
            logger.error(f"Unknown outcome type: {ret}")
            outcome_type_int = 0
        return OUTCOME_TYPE[outcome_type_int]
    

    def query_time_dict_from_value(self, time_value: str) -> str:
        '''
        Ask the LLM to dissect the time value into the actual value and the unit.
        '''
        extra_vars = {
            "Value": time_value,
            "Template": self.get_json_template_string_for_data_extraction(TIME_VALUE_HEADERS)
        }
        return self.invoke_prompt_on_text(name=f"value and units from time value \"{time_value}\"", prompt_name="PromptGenericDataFormat", text="", text_context="LLM", extra_vars=extra_vars)


    def query_clinical_data(self, headers: List[str], outcome: str, outcome_type: str, treatment_arm: str, time_value: str, stat_group: Dict[str, str], text: str, text_context: str) -> str:
        '''
        Construct the prompt(s) to get some clinical data from the page using the LLM.
        '''
        clinical_json = self.get_json_template_string_for_data_extraction(headers)
        stat_group_text = ""
        for key, val in stat_group.items():
            if NO_DATA in val:
                continue
            header_dict = self.definitions.get_field_by_name(key)
            header_label = header_dict['Field Label']
            stat_group_text += f"{header_label.lower()}: {val}, "
        stat_group_text = stat_group_text.strip().strip(",")
        name = f"clinical data for {outcome} with {treatment_arm} for {time_value} and {stat_group_text}"
        extra_vars = {
            "Outcome": outcome,
            "Outcome_Type": outcome_type,
            "Treatment_Arm": treatment_arm,
            "Time_Value": time_value,
            "Stat_Group": stat_group_text,
            "Template": clinical_json,
        }
        return self.invoke_prompt_on_text(name=name, prompt_name="PromptClinical", text=text, text_context=text_context, extra_vars=extra_vars, keep_no_data_response=True)
