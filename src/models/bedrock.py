
import logging
import sys

import boto3
from botocore.exceptions import ClientError

from .llm import Llm

logger = logging.getLogger(__name__)

class BedrockLlm(Llm):
    '''
    This is the base class for any API LLM that is using Amazon Bedrock.
    '''

    MODEL_ID = None
    CREDENTIAL_PROFILE = "capstone"
    SERVICE = "bedrock-runtime"
    REGION = "us-east-1"

    def __init__(self):
        super().__init__()

        try:
            bedrock_session = boto3.Session(profile_name=self.CREDENTIAL_PROFILE)
            self.client = bedrock_session.client(service_name=self.SERVICE, region_name=self.REGION)
        except ClientError as e:
            logger.error('Error getting Amazon Bedrock client, have you put your credentials in "~/.aws/credentials" and "~/.aws/config" yet? Use profile name "capstone".')
            raise e
        
    def get_invoke_body(self, prompt):
        return prompt
    
    def process_response(self, response):
        return response

    def invoke(self, prompt):
        try:
            # The different model providers have individual request and response formats.

            body = self.get_invoke_body(prompt)
            logger.info(f"Invoking model with request size of {sys.getsizeof(body)} bytes")

            response = self.client.invoke_model(
                modelId=self.MODEL_ID, body=body,
            )

            return self.process_response(response)

        except ClientError:
            logger.error("Couldn't invoke the model!")
            raise