
from .mistral import Mistral

class Mixtral8x7bInstruct(Mistral):
    '''
    This is the Mixtral (not a misspelling) 8x7B Instruct model with 32k max tokens.
    https://aws.amazon.com/bedrock/pricing/
 
    Instantiate this class, then call "invoke(<prompt>)" to get responses.
    '''

    MODEL_ID: str = "mistral.mixtral-8x7b-instruct-v0:1"

    INPUT_TOKEN_PRICE_PER_1K: float = 0.00015
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0.0002