
import logging
import json
from typing import List, Optional

from .bedrock import BedrockLlm

logger = logging.getLogger(__name__)


class Llama2(BedrockLlm):
    '''
    This is the Meta Llama 2 model.
    https://aws.amazon.com/bedrock/pricing/
    '''

    MODEL_ID: Optional[str] = None

    INPUT_TOKEN_PRICE_PER_1K: float = 0
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0

    PARAMETERS: List[str] = [
        "temperature",
        "top_p",
        "max_gen_len",
    ]

    total_input_tokens: Optional[int] = 0
    total_output_tokens: Optional[int] = 0


    def set_parameters_from_config(self, config):
        '''
        Sets model parameters from a config.

        Parameters:
            config (Dict[str, Dict])
        '''
        try:
            llm_section = config["LLM"]
            temperature = float(llm_section["Temperature"])
            top_p = float(llm_section["NucleusSampling"])
            max_gen_len = int(llm_section["MaxGenerationLength"])
        except KeyError as e:
            logger.error("Section or value is missing in configuration! Make sure you didn't delete anything important!")
            raise e
        except ValueError as e:
            logger.error("Invalid value in configuration!")
            raise e
        
        self.set_parameters(temperature=temperature, top_p=top_p, max_gen_len=max_gen_len)


    def get_invoke_body(self, prompt):
        '''
        From a string prompt, form the input body that is to be passed to the model.

        Parameters:
            prompt (str)

        Returns:
            str
        '''
        return json.dumps(
            {
                "prompt": prompt,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_gen_len": self.max_gen_len,
            }
        )
    
    def process_response(self, response):
        '''
        This function does any post-processing that is immediately needed to convert the model output
        into something usable to us.

        Parameters:
            response (Dict[str, Any])

        Returns:
            str
        '''
        body = json.loads(response["body"].read())
        completion = body["generation"]
        prompt_token_count = body["prompt_token_count"]
        generation_token_count = body["generation_token_count"]
        stop_reason = body["stop_reason"]
        logger.debug(f"Prompt tokens: {prompt_token_count + generation_token_count} (Input: {prompt_token_count}, Output: {generation_token_count}). Stop reason: {stop_reason}")
        self.total_input_tokens += prompt_token_count
        self.total_output_tokens += generation_token_count
        price_estimate = (self.total_input_tokens / 1000) * self.INPUT_TOKEN_PRICE_PER_1K + (self.total_output_tokens / 1000) * self.OUTPUT_TOKEN_PRICE_PER_1K
        logger.debug(f"Total input tokens: {self.total_input_tokens}, total output tokens: {self.total_output_tokens}, total price estimate: ${price_estimate:.2f}")
        return completion.strip()