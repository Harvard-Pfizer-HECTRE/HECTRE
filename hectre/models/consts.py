from hectre.models.claude3haiku import Claude3Haiku
from hectre.models.llama2_13b_chat import Llama213bChatLlm
from hectre.models.llama2_70b_chat import Llama270bChatLlm
from hectre.models.mistral_7b_instruct import Mistral7bInstruct
from hectre.models.mixtral_8x7b_instruct import Mixtral8x7bInstruct

NAME_TO_MODEL_CLASS = {
    "Claude3Haiku": Claude3Haiku,
    "Llama213bChat": Llama213bChatLlm,
    "Llama270bChat": Llama270bChatLlm,
    "Mistral7bInstruct": Mistral7bInstruct,
    "Mixtral8x7bInstruct": Mixtral8x7bInstruct,
}