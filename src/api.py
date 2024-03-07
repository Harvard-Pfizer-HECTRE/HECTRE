import logging

from .lib.extractor import Extractor
from .lib.parse_config import Config

logger = logging.getLogger(__name__)

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
    extractor.extract()
    
    # TODO the rest