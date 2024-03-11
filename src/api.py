import logging

from picos import Picos
from .lib.hectre import Hectre

logger = logging.getLogger(__name__)

# Global HECTRE singleton
hectre = None

def invoke_model(prompt):
    '''
    Invoke the model, following the configuration file.
    This is mostly just used for testing.

    Parameters:
        prompt (str): The prompt for the model.

    Returns:
        str: The output from the model.
    '''
    global hectre
    if hectre is None:
        hectre = Hectre()

    return hectre.invoke_model(prompt)


def extract_data(pdfObject, Picos):
    '''
    Main entry function that is called by the front end to initiate the extraction
    process.
    TODO: Finish this function up

    Parameters:
        pdfObject TODO
        picosObject TODO

    Returns:
        No output. This function will take a while, so we will store the output elsewhere.
    '''
    