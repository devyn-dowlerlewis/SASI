from pydantic import BaseModel


class ParametersModel(BaseModel):
    system_message: str
