
import logging
import json

from .bedrock import BedrockLlm

logger = logging.getLogger(__name__)

class Llama2(BedrockLlm):
    '''
    This is the Meta Llama 2 model.
    https://aws.amazon.com/bedrock/pricing/
    '''

    MODEL_ID = None

    def __init__(self):
        super().__init__()
        self.set_default_parameters()

    def set_default_parameters(self):
        '''
        Sets the default parameters. The config file will override this.
        '''
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
        '''
        Sets custom parameters.

        Parameters:
            temperature (float)
            top_p (float)
            max_gen_len (int)
        '''
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
        
        self.set_parameters(temperature, top_p, max_gen_len)

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
        logger.debug(f"Total tokens: {prompt_token_count + generation_token_count} (Input: {prompt_token_count}, Output: {generation_token_count}). Stop reason: {stop_reason}")
        return completion