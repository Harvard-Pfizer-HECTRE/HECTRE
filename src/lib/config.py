import configparser
import os

class Config:
    def __init__(self):
        self.get_config()
    
    def __getitem__(self, item):
        '''
        Make this class act as a subscriptable dictionary.
        '''
        return self.config[item]

    def get_config(self):
        '''
        Parses the configuration in the config.ini and store it in this object, as well as return it.

        Returns:
            Dict[str, Dict]
        '''
        if not getattr(self, "config", None):
            config_path = os.path.join(os.path.dirname(__file__), "../../config.ini")
            config = configparser.ConfigParser()
            config.read(config_path)
            self.config = config
        return self.config