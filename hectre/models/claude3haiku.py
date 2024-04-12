
from hectre.models.anthropic import AnthropicLlm

class Claude3Haiku(AnthropicLlm):
    '''
    This is the Anthropic's Claude 3 Haiku LLM.
    It is the cheapest LLM from Anthropic, and does quite well.
    It has a context window of 200k.
 
    Instantiate this class, then call "invoke(<prompt>)" to get responses.
    '''
    USER_ASSISTANT_MODEL: bool = True

    MODEL_ID: str = "anthropic.claude-3-haiku-20240307-v1:0"

    INPUT_TOKEN_PRICE_PER_1K: float = 0.00025
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0.00125
