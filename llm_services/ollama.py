from openai import OpenAI
import instructor


# noinspection PyProtectedMember
class Ollama:
    def __init__(self):
        self.client = instructor.patch(OpenAI(base_url="http://192.168.1.161:11434/v1", api_key="ollama"), mode=instructor.Mode.JSON)


    def make_request(self, message_array, model, response_model):
        print(model)
        print(message_array)
        try:
            response = self.client.chat.completions.create(
                model=model,
                response_model=response_model,
                messages=message_array,
                max_retries=5,
                temperature=0
            )
            usage = response._raw_response.usage
            usage_dict = {attr: getattr(usage, attr) for attr in ['completion_tokens', 'prompt_tokens', 'total_tokens']}

            response_dict = response.to_dict()
            response_dict["usage"] = usage_dict

            return response_dict  # Return the raw response

        except Exception as e:
            print(f"Error in make_request: {e}")
            return {"error": e}
