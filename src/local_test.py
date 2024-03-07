
import logging
import sys

from models.llama2_13b import Llama213bLlm

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    model = Llama213bLlm()
    response = model.invoke("how are you today?")
    print(response)