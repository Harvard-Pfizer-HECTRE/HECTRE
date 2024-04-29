from pydantic import BaseModel


class ExtractionRequest(BaseModel):
    folder_id: str
    outcomes_string: str
