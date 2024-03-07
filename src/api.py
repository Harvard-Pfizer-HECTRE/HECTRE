import logging

from .lib.extractor import Extractor
from .lib.parse_config import Config

logger = logging.getLogger(__name__)

def invoke_model(prompt):
    '''
    Invoke the model, following the configuration file.
    This is mostly just used for testing.
    '''
    try:
        config = Config().get_config()
    except Exception as e:
        logger.error("Unable to read config file!")
        raise e
    
    extractor = Extractor()
    extractor.set_config(config)
    return extractor.invoke_model(prompt)


def extract_data(pdfObject, picosObject):
    try:
        config = Config().get_config()
    except Exception as e:
        logger.error("Unable to read config file!")
        raise e
    
    extractor = Extractor()
    extractor.set_config(config)
    extractor.set_pdf(pdfObject)
    extractor.set_picos(picosObject)
    # TODO the rest
    extractor.extract()
    