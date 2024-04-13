from .prompts import create_message_array
from .response_model import ResponseModel


class _Template:
    def __init__(self):
        self.default_error_dict = {
            "request_state": "error",
            "dtmfNavigationOptions": [],
            "explanation": "Empty System Prompt",
            "navigation_options_presented": False,
            "account_info_presented_to_user": False,
            "usage": {
                "completion_tokens": 0,
                "prompt_tokens": 0,
                "total_tokens": 0
            }
        }

    def generate_response(self, request_data, client_instance):
        try:
            print(request_data)
            system_message = request_data.parameters["system_message"]
            model = request_data.model
            if system_message == "":
                return self.default_error_dict

            message_array = create_message_array(system_message)
            raw_response = client_instance.make_request(message_array, model, ResponseModel)

            print(raw_response)
            return raw_response

        except Exception as e:
            print(e)
            return {"error": str(e)}
