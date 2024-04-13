from openai import AzureOpenAI
import instructor
import os
import time

# noinspection PyProtectedMember
class AzureOpenAi:
    def __init__(self):
        self.client = instructor.patch(AzureOpenAI(api_key=os.environ.get("AZURE_OPENAI_API_KEY"), azure_endpoint = "https://connex-gpt-northc.openai.azure.com/", api_version = "2024-03-01-preview"))

    def make_request(self, message_array, gpt_version, response_model):
        model = map_gpt_version(gpt_version)
        print(model)
        print(message_array)
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=model,
                response_model=response_model,
                messages=message_array,
                temperature=0,
                max_retries=5
            )
            end_time = time.time()
            usage = response._raw_response.usage
            usage_dict = {attr: getattr(usage, attr) for attr in ['completion_tokens', 'prompt_tokens', 'total_tokens']}

            response_dict = response.to_dict()
            response_dict["usage"] = usage_dict
            print(f"\nRequest to {model} took {end_time - start_time} seconds. Usage:")
            print(usage_dict, "\n")

            return response_dict  # Return the raw response

        except Exception as e:
            print(f"Error in make_request: {e}")
            end_time = time.time()
            print(f"\nFailed Request to {model} took {end_time - start_time} seconds\n")
            return {"error": e}


def map_gpt_version(gpt_version):
    #return "gpt-4-0125-preview"
    if gpt_version == "gpt4":
        return "gpt-4-0125"
    else:
        return "gpt-35-0125"
