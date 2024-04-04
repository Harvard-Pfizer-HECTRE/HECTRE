
from .mistral import Mistral

class Mistral7bInstruct(Mistral):
    '''
    This is the Mistral 7B Instruct model with 32k max tokens.
    https://aws.amazon.com/bedrock/pricing/
 
    Instantiate this class, then call "invoke(<prompt>)" to get responses.
    '''

    MODEL_ID: str = "mistral.mistral-7b-instruct-v0:2"

    INPUT_TOKEN_PRICE_PER_1K: float = 0.00015
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0.0002
