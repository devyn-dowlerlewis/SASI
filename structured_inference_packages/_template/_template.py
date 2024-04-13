from .prompts import create_message_array
from .response_model import ResponseModel


class _Template:
    def generate_response(self, request_data, service_instance):
        try:
            #print(request_data)

            parameters = request_data.parameters
            message_array = create_message_array(parameters)
            raw_response = service_instance.make_request(message_array, request_data.model, ResponseModel)

            #print(raw_response)
            return raw_response

        except Exception as e:
            print(e)
            return {"error": str(e)}
