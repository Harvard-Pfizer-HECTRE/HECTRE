
from ..models.consts import NAME_TO_MODEL_CLASS
from .config import Config

class HectreException(Exception):
    pass

class Hectre:
    def __init__(self):
        self.config = Config()
        try:
            llm_name = self.config["LLM"]["LLMName"]
        except KeyError:
            raise HectreException("Could not find LLMName in configuration!")
        self.set_llm(llm_name)
        self.llm.set_parameters_from_config(self.config)

    def set_llm(self, llm_name):
        '''
        Set the LLM to be used by HECTRE.

        Parameters:
            llm_name (str)
        '''
        try:
            self.llm = NAME_TO_MODEL_CLASS[llm_name]()
        except KeyError:
            raise HectreException(f"{llm_name} is not a supported LLM type!")
        
    def invoke_model(self, prompt):
        '''
        Call the LLM to get an output.

        Parameters:
            prompt (str)

        Returns:
            str
        '''
        return self.llm.invoke(prompt)