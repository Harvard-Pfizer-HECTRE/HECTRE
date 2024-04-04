
import logging
import json
from typing import Optional

from .bedrock import BedrockLlm

logger = logging.getLogger(__name__)

class Mistral(BedrockLlm):
    '''
    This is the Mistral AI model.
    https://aws.amazon.com/bedrock/pricing/
    '''

    MODEL_ID: Optional[str] = None

    INPUT_TOKEN_PRICE_PER_1K: float = 0
    OUTPUT_TOKEN_PRICE_PER_1K: float = 0

    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[float] = None
    max_tokens: Optional[float] = None

    total_input_tokens: Optional[int] = 0
    total_output_tokens: Optional[int] = 0

    def __init__(self):
        super().__init__()
        self.set_default_parameters()

    def set_default_parameters(self):
        '''
        Sets the default parameters. The config file will override this.
        '''
        self.temperature = 0
        self.top_p = 0
        self.top_k = 0
        self.max_tokens = 0

    def set_parameters(self, temperature=None, top_p=None, top_k=None, max_tokens=None):
        '''
        Sets custom parameters.

        Parameters:
            temperature (float)
            top_p (float)
            max_gen_len (int)
        '''
        # Set custom paramaters if you want to, prior to calling invoke()
        if temperature is not None:
            logger.debug(f"Set model temperature={temperature}")
            self.temperature = temperature
        if top_p is not None:
            logger.debug(f"Set model top_p={top_p}")
            self.top_p = top_p
        if top_k is not None:
            logger.debug(f"Set model top_k={top_k}")
            self.top_k = top_k
        if max_tokens is not None:
            logger.debug(f"Set model max_tokens={max_tokens}")
            self.max_tokens = max_tokens

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
            top_k = int(llm_section["TopTokens"])
            max_tokens = int(llm_section["MaxGenerationLength"])
        except KeyError as e:
            logger.error("Section or value is missing in configuration! Make sure you didn't delete anything important!")
            raise e
        except ValueError as e:
            logger.error("Invalid value in configuration!")
            raise e
        
        self.set_parameters(temperature, top_p, top_k, max_tokens)

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
                "top_k": self.top_k,
                "max_tokens": self.max_tokens,
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
        completion = body["outputs"][0]["text"]
        stop_reason = body["outputs"][0]["stop_reason"]
        logger.debug(f"Stop reason: {stop_reason}")
        return completion.strip()