
import logging
import json

from .bedrock import BedrockLlm

logger = logging.getLogger(__name__)

class Llama213bLlm(BedrockLlm):
    '''
    This is the Meta Llama 2 model with 13b tokens.
    This is the cheapest variant.
    When used through Amazon Bedrock, as of writing the fees are:
    $0.00075 per 1,000 input tokens, and
    $0.00100 per 1,000 output tokens.
    https://aws.amazon.com/bedrock/pricing/
 
    Instantiate this class, then call "invoke(<prompt>)" to get responses.
    '''

    MODEL_ID = "meta.llama2-13b-chat-v1"

    def __init__(self):
        super().__init__()
        self.set_default_parameters()

    def set_default_parameters(self):
        # Use a lower value to decrease randomness in the response.
        # The default is 0.5.
        self.temperature = 0.3
        # Use a lower value to ignore less probable options. Set to 0 or 1.0 to disable.
        # The default is 0.9.
        self.top_p = 0.5
        # Specify the maximum number of tokens to use in the generated response. The model truncates the response once the generated text exceeds max_gen_len.
        # The default is 512.
        self.max_gen_len = 512

    def set_parameters(self, temperature=None, top_p=None, max_gen_len=None):
        # Set custom paramaters if you want to, prior to calling invoke()
        if temperature is not None:
            logger.info(f"Set model temperature={temperature}")
            self.temperature = temperature
        if top_p is not None:
            logger.info(f"Set model top_p={top_p}")
            self.top_p = top_p
        if max_gen_len is not None:
            logger.info(f"Set model max_gen_len={max_gen_len}")
            self.max_gen_len = max_gen_len

    def get_invoke_body(self, prompt):
        return json.dumps(
            {
                "prompt": prompt,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_gen_len": self.max_gen_len,
            }
        )
    
    def process_response(self, response):
        body = json.loads(response["body"].read())
        completion = body["generation"]
        prompt_token_count = body["prompt_token_count"]
        generation_token_count = body["generation_token_count"]
        stop_reason = body["stop_reason"]
        logger.info(f"Total tokens: {prompt_token_count + generation_token_count} (Input: {prompt_token_count}, Output: {generation_token_count}). Stop reason: {stop_reason}")
        return completion