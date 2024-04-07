
import logging
import sys
from typing import Any, List, Optional

import boto3
from botocore.exceptions import ClientError

from ..consts import (
    AWS_PROFILE,
    AWS_REGION,
    LLM_BEGIN_PROMPT_LOGGING_INDICATOR,
    LLM_BEGIN_RESPONSE_LOGGING_INDICATOR,
    LLM_END_PROMPT_LOGGING_INDICATOR,
    LLM_END_RESPONSE_LOGGING_INDICATOR,
)
from .llm import Llm

logger = logging.getLogger(__name__)


class BedrockLlm(Llm):
    '''
    This is the base class for any API LLM that is using Amazon Bedrock.
    '''

    MODEL_ID: Optional[str] = None
    CREDENTIAL_PROFILE: str = AWS_PROFILE
    SERVICE: str = "bedrock-runtime"
    REGION: str = AWS_REGION

    client: Any = None


    def __init__(self):
        super().__init__()

        logger.debug(f"Using model ID {self.MODEL_ID}")

        try:
            bedrock_session = boto3.Session(profile_name=self.CREDENTIAL_PROFILE)
            self.client = bedrock_session.client(service_name=self.SERVICE, region_name=self.REGION)
        except ClientError as e:
            logger.error('Error getting Amazon Bedrock client, have you put your credentials in "~/.aws/credentials" and "~/.aws/config" yet? Use profile name "capstone".')
            raise e
        

    def get_invoke_body(self, prompt: str) -> Any:
        return prompt
    

    def process_response(self, response: Any) -> str:
        return response


    def invoke(self, prompt: List[str]) -> str:
        '''
        Invokes the model, and returns a response.

        Parameters:
            prompt (str): The prompt for the model.

        Returns:
            str: The model response.
        '''
        try:
            # The different model providers have individual request and response formats.

            body = self.get_invoke_body(prompt)
            logger.debug(f"Invoking model with request size of {sys.getsizeof(body)} bytes")
            logged_prompt = '\n'.join(prompt)
            logger.debug(f"{LLM_BEGIN_PROMPT_LOGGING_INDICATOR}{logged_prompt}{LLM_END_PROMPT_LOGGING_INDICATOR}")

            response = self.client.invoke_model(
                modelId=self.MODEL_ID, body=body,
            )

            processed_response = self.process_response(response)
            logger.debug(f"{LLM_BEGIN_RESPONSE_LOGGING_INDICATOR}{processed_response}{LLM_END_RESPONSE_LOGGING_INDICATOR}")
            return processed_response

        except ClientError:
            logger.error("Couldn't invoke the model!")
            raise