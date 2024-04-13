from pydantic import BaseModel


class RequestModel(BaseModel):
    service: str
    model: str
    function: str
    parameters: dict
