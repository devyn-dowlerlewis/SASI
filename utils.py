import importlib
from pydantic import ValidationError
from sasi_request_model import RequestModel


def get_parameters_model(function_value: str):
    try:
        # Import the ParametersModel from the module based on function_value
        parameters_module = importlib.import_module(f"structured_inference_packages.{function_value}.parameters_model")
    except ModuleNotFoundError:
        return None

    ParametersModel = getattr(parameters_module, "ParametersModel", None)
    return ParametersModel


def validate_request_model(req_data):
    try:
        return RequestModel(**req_data), None
    except ValidationError as e:
        return None, e


def validate_parameters_model(req_model):
    ParametersModel = get_parameters_model(req_model.function)
    if ParametersModel:
        try:
            parameters = ParametersModel(**req_model.parameters)
            return parameters, None
        except ValidationError as e:
            return None, e
    return None, f"No parameters model found for function: {req_model.function}"


def instantiate_function_class(req_model):
    function_class_name = format_class_name(req_model.function)
    try:
        function_module = importlib.import_module(f"structured_inference_packages.{req_model.function}.{req_model.function}")
        function_class = getattr(function_module, function_class_name, None)
        if function_class:
            return function_class(), None
    except ImportError as e:
        pass
    return None, f"No function class found for function: {req_model.function}"


def instantiate_client(req_model):
    client_class_name = format_class_name(req_model.client)  # Assuming client naming follows a similar pattern
    try:
        # Assuming all clients are structured similarly under the llm_services directory
        client_module = importlib.import_module(f"llm_services.{req_model.client}")
        # Assuming a consistent class naming convention or a consistent class name within each client module
        client_class = getattr(client_module, client_class_name, None)
        if client_class:
            return client_class(), None  # Successfully instantiated client, no error
    except ImportError as e:
        # Logging the error might be helpful for debugging
        print(f"Error importing client {req_model.client}: {e}")

    # If we reach this point, there was an issue with importing or finding the client class
    return None, f"No client class found for client: {req_model.client}"


def format_class_name(s):
    # Identify leading underscores
    leading_underscores = ''.join('_' for _ in s[:len(s) - len(s.lstrip('_'))])
    # Remove leading underscores for processing
    s_trimmed = s.lstrip('_')
    # Split the string by underscores, capitalize each part, then rejoin with underscores removed
    parts = s_trimmed.split('_')
    formatted_parts = [part.capitalize() for part in parts if part]  # Ensure part is not empty
    formatted_name = ''.join(formatted_parts)

    return f"{leading_underscores}{formatted_name}"


