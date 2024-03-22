from .api import invoke_model


'''
This file is used for basic testing of invoking the LLM.
TODO: Move this to a unit test.
'''


if __name__ == '__main__':
    response = invoke_model("How are you today?")
    print(response)
    response = invoke_model("Tell me that I will pass my capstone class. Give me a one sentence reply.")
    print(response)