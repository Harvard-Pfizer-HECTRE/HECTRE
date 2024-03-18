from .llama2_13b import Llama213bLlm
from .llama2_70b import Llama270bLlm

NAME_TO_MODEL_CLASS = {
    "Llama213b": Llama213bLlm,
    "Llama270b": Llama270bLlm,
}