from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SystemRequestStateEnum(Enum):
    DTMF_NAVIGATION_REQUEST = "DTMF Navigation Request"
    PERSONAL_INFORMATION_REQUEST = "Personal Information Request"
    OTHER = "Other"


class DTMFNavigationOption(BaseModel):
    dtmfKey: str
    description: str


class ResponseModel(BaseModel):
    request_state: SystemRequestStateEnum = Field(description="The current request state of the DTMF system. If the system requests a multi-digit input it's a personal information request.")
    navigation_options_presented: bool = Field(description="Whether or not the last system message explicitly presented the user with dtmf navigation options")
    dtmfNavigationOptions: Optional[List[DTMFNavigationOption]] = Field(default=None, description="A list of dtmf navigation options.")
    account_info_presented_to_user: bool = Field(description="Whether or not the system provided account information such as balance or transaction information to the user in the system message.")
    explanation: str = Field(description="Explanation of state choice")

    def to_dict(self):
        return {
            "request_state": self.request_state.value,  # Convert enum to string
            "dtmfNavigationOptions": [
                {"dtmfKey": option.dtmfKey, "description": option.description} for option in self.dtmfNavigationOptions
            ] if self.dtmfNavigationOptions else [],
            "explanation": self.explanation,
            "navigation_options_presented": self.navigation_options_presented,
            "account_info_presented_to_user": self.account_info_presented_to_user
        }


