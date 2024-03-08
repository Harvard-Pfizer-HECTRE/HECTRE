

class Llm:
    '''
    A generic LLM class.
    '''
    def __init__(self):
        pass

    def set_parameters_from_config(self, config):
        pass

    def invoke(self, prompt):
        raise NotImplementedError