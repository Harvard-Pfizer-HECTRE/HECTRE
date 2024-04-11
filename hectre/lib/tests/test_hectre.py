import pytest

from hectre.lib.hectre import Hectre
from hectre.models.consts import NAME_TO_MODEL_CLASS


def test_hectre_init():
    """
    Check we can init HECTRE, since it does a lot.
    """
    hectre = Hectre()
    pytest.hectre = hectre


def test_invoke_all_llms():
    """
    Check that all the installed LLMs work.
    It is easier to test that here, than in the models folder.
    """
    for name in NAME_TO_MODEL_CLASS.keys():
        pytest.hectre.set_llm(name)
        # Set a low response token count
        pytest.hectre.config["LLM"]["MaxGenerationLength"] = 10
        pytest.hectre.llm.set_parameters_from_config(pytest.hectre.config)
        pytest.hectre.invoke_model(["Hello world!"])