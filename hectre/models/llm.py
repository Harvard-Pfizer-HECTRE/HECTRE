import logging

from pydantic import BaseModel
from typing import Any, List

logger = logging.getLogger(__name__)


class LlmException(Exception):
    pass


class Llm(BaseModel, extra='allow'):
    '''
    A generic LLM class.
    '''
    PARAMETERS: List[str] = []
    
    # Some models, such as Claude 3, are designed as user-assistant models, not just text completion
    USER_ASSISTANT_MODEL: bool = False


    def __init__(self):
        super().__init__()
        self.set_default_parameters()


    def set_default_parameters(self):
        '''
        Sets the default parameters. The config file will override this.
        '''
        for key in self.PARAMETERS:
            setattr(self, key, 0)


    def set_parameters(self, **kwargs):
        '''
        Sets custom parameters for the model.
        '''
        for key, val in kwargs.items():
            if key not in self.PARAMETERS:
                logger.error(f"Invalid parameter {key}!")
                raise LlmException(f"Invalid parameter {key}!")
            logger.debug(f"Set model {key}={val}")
            setattr(self, key, val)


    def set_parameters_from_config(self, config: Any):
        pass


    def invoke(self, prompt: str):
        raise NotImplementedError()