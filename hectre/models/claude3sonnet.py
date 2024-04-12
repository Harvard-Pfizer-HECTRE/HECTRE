
from hectre.models.anthropic import AnthropicLlm

class Claude3Sonnet(AnthropicLlm):
    '''
    This is the Anthropic's Claude 3 Sonnet LLM.
    It is the medium-sized LLM from Anthropic.
    It has a context window of 200k.
 
    Instantiate this class, then call "invoke(<prompt>)" to get responses.
    '''
    USER_ASSISTANT_MODEL: bool = True

    MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"

    INPUT_TOKEN_PRICE_PER_1K: float = 0.003
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0.015
