from pydantic import BaseModel


class RequestModel(BaseModel):
    client: str
    model: str
    function: str
    parameters: dict
