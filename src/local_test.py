
import logging
import sys

from .api import invoke_model

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    response = invoke_model("How are you today?")
    print(response)
    response = invoke_model("Tell me that I will pass my capstone class. Give me a one sentence reply.")
    print(response)