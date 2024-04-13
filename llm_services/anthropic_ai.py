import anthropic
import instructor
import time


class AnthropicAi:
    def __init__(self):
        self.client = instructor.from_anthropic(anthropic.Anthropic())

    def make_request(self, message_array, model, response_model):
        #print(message_array)
        model = self.map_model(model)
        print(f"\nService: Anthropic AI | Model: {model}")
        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=model,
                response_model=response_model,
                messages=message_array,
                temperature=0.1,
                max_retries=5,
                max_tokens=4096
            )
            print(response)
            usage = response._raw_response.usage
            usage_dict = {attr: getattr(usage, attr) for attr in ['input_tokens', 'output_tokens']}

            response_dict = response.to_dict()
            response_dict["usage"] = usage_dict
            end = time.time()
            print(f"Inference Complete In {end - start:.3f} Seconds. Usage: {usage_dict}")
            return response_dict  # Return the raw response

        except Exception as e:
            print(f"Error in make_request: {e}")
            return {"error": e}


    def map_model(self, model):
        #print(model.lower())
        if model.lower() == "opus":
            return "claude-3-opus-20240229"
        elif model.lower() == "sonnet":
            return "claude-3-sonnet-20240229"
        else:
            return "claude-3-haiku-20240307"
