
from hectre.models.meta import MetaLlm

class Llama270bChatLlm(MetaLlm):
    '''
    This is the Meta Llama 2 model with 70b tokens.
    This is more expensive than the 13b variant, but more powerful.
    It is about 2.5x pricier.
    https://aws.amazon.com/bedrock/pricing/
 
    Instantiate this class, then call "invoke(<prompt>)" to get responses.
    '''

    MODEL_ID: str = "meta.llama2-70b-chat-v1"

    INPUT_TOKEN_PRICE_PER_1K: float = 0.00195
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0.00256
