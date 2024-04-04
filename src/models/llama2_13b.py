
from .llama2 import Llama2

class Llama213bLlm(Llama2):
    '''
    This is the Meta Llama 2 model with 13b tokens.
    This is the cheapest variant.
    When used through Amazon Bedrock, as of writing the fees are:
    $0.00075 per 1,000 input tokens, and
    $0.00100 per 1,000 output tokens.
    https://aws.amazon.com/bedrock/pricing/
 
    Instantiate this class, then call "invoke(<prompt>)" to get responses.
    '''

    MODEL_ID: str = "meta.llama2-13b-chat-v1"

    INPUT_TOKEN_PRICE_PER_1K: float = 0.00075
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0.001
