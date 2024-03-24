from pydantic import BaseModel

class Llm(BaseModel):
    '''
    A generic LLM class.
    '''
    def set_parameters_from_config(self, config):
        pass

    def invoke(self, prompt):
        raise NotImplementedError()