from openai import OpenAI
import instructor
import time

# noinspection PyProtectedMember
class OpenAi:
    def __init__(self):
        self.client = instructor.patch(OpenAI())

    def make_request(self, message_array, gpt_version, response_model):
        model = map_gpt_version(gpt_version)
        print(f"\nService: Open AI | Model: {model}")
        # print(message_array)
        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=model,
                response_model=response_model,
                messages=message_array,
                temperature=0
            )
            print(response)
            usage = response._raw_response.usage
            usage_dict = {attr: getattr(usage, attr) for attr in ['completion_tokens', 'prompt_tokens', 'total_tokens']}

            response_dict = response.to_dict()
            response_dict["usage"] = usage_dict
            end = time.time()
            print(f"Inference Complete In {end - start:.3f} Seconds. Usage: {usage_dict}")

            return response_dict  # Return the raw response

        except Exception as e:
            print(f"Error in make_request: {e}")
            return {"error": e}


def map_gpt_version(gpt_version):
    #return "gpt-4-0125-preview"
    if gpt_version == "gpt4":
        return "gpt-4-0125-preview"
    else:
        return "gpt-3.5-turbo-0125"
