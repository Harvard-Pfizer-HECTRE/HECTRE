import os

from pydantic import BaseModel
from typing import Any, Optional
import yaml


class Config(BaseModel):
    '''
    This class instantiates an object with the config.YAML configuration file, and is used
    by HECTRE to set certain parameters, such as what LLM to use, and LLM parameters.
    '''
    config: Optional[Any] = None


    def __init__(self):
        super().__init__()
        self.config = self.get_config()
    

    def __getitem__(self, item):
        '''
        Make this class act as a subscriptable dictionary.
        '''
        return self.config[item]


    def get_config(self):
        '''
        Parses the configuration in the config.yaml and store it in this object, as well as return it.

        Returns:
            Dict[str, Dict]
        '''
        if not self.config:
            config_path = os.path.join(os.path.dirname(__file__), "../../config.yaml")
            with open(config_path) as f:
                config = yaml.safe_load(f)
            return config
        return self.config