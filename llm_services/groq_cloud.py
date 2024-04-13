from groq import Groq
import os
import instructor


# noinspection PyProtectedMember
class GroqCloud:
    def __init__(self):
        self.client = instructor.patch(Groq(api_key=os.environ.get("GROQ_API_KEY")), mode=instructor.Mode.MD_JSON)

    def make_request(self, message_array, model, response_model):
        print(message_array)
        try:
            response: response_model = self.client.chat.completions.create(
                model=model,
                response_model=response_model,
                messages=message_array,
                temperature=0.1,
                max_retries=5
            )
            print(response)
            usage = response._raw_response.usage
            usage_dict = {attr: getattr(usage, attr) for attr in ['completion_tokens', 'prompt_tokens', 'total_tokens']}

            response_dict = response.to_dict()
            response_dict["usage"] = usage_dict

            return response_dict  # Return the raw response

        except Exception as e:
            print(f"Error in make_request: {e}")
            return {"error": e}