
import logging
import sys

from .api import invoke_model

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    response = invoke_model("how are you today?")
    print(response)